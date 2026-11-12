import os,sys,tempfile,time,json,cProfile,pstats,io,resource,builtins
from pathlib import Path
from unittest import mock
import numpy as np
R=Path('/workspace/audit-v0.9.39/OandG_Workbench_v0.9.39');sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import project as P
from ogmap import perf,project as MP,grids,georef
from ogmap.window import MapWindow
from test_project_assets import a_grid
from test_map_images import make_image
import tkinter as tk
from tkinter import messagebox
for n in ('showinfo','showwarning','showerror'):setattr(messagebox,n,lambda *a,**k:None)
active={'counts':None}
def audit_event(event,args):
 if event=='open' and active['counts'] is not None:
  mode=args[1] if len(args)>1 else None
  if isinstance(mode,str) and ('r' in mode or '+' in mode):active['counts']['file_read_open_events']+=1
sys.addaudithook(audit_event)
real_reader=ProjectDatabase.reader
def reader(*a,**kw):
 d=real_reader(*a,**kw)
 def trace(sql):
  if active['counts'] is not None and sql.lstrip().upper().startswith(('SELECT','WITH')):active['counts']['worker_selects']+=1
 d.connection.set_trace_callback(trace);return d
ProjectDatabase.reader=staticmethod(reader)
n=int(sys.argv[1]);out=Path('/workspace/audit-v0.9.39');results=[]
def rss():
 return int(next(x.split()[1] for x in Path('/proc/self/status').read_text().splitlines() if x.startswith('VmRSS:')))/1024
with tempfile.TemporaryDirectory() as td:
 p=P.Project.create(Path(td),'Scale');db=ProjectDatabase(p.database_path);db.set_project_value('coordinate_system','EPSG:32613')
 stamp='2026-11-12T00:00:00+00:00'
 with db.transaction() as c:
  c.executemany('INSERT INTO wells(id,well_uid,well_name,api_uwi,created_at,updated_at,well_symbol_code,well_number) VALUES (?,?,?,?,?,?,?,?)',((i+1,f'GW-{i}',f'Well {i}',f'49{i:012}',stamp,stamp,'DH99' if i%17==0 else 'LOC',str(i+1)) for i in range(n)))
  c.executemany('INSERT INTO locations(well_id,surface_x,surface_y) VALUES (?,?,?)',((i+1,500000+(i%1000)*100,4800000+(i//1000)*100) for i in range(n)))
 g=a_grid();gid=grids.save(db,g)
 img=georef.import_image(db,make_image(Path(td)/'plat.png'),'Plat');img.points=[georef.ControlPoint(0,0,500000,4800000),georef.ControlPoint(200,0,502000,4800000),georef.ControlPoint(0,100,500000,4799000)];img.solve();georef.save(db,img)
 import shapefile
 for k in range(250):
  shape=Path(td)/f'Layer{k}.shp'
  with shapefile.Writer(str(shape),shapeType=shapefile.POLYLINE) as writer:
   writer.field('NAME','C')
   for j in range(5):
    x=500000+k*200;y=4800000+j*100
    writer.line([[(x,y),(x+1000,y+2000)]]);writer.record(f'Line {k}-{j}')
  MP.add_layer(db,shape)
 root=tk.Tk();root.withdraw();win=None
 def settle():
  for _ in range(4):win.update()
 def measure(label,fn):
  reads={'n':0};orig=builtins.open;draws=win.view.draws if win else 0;profile=cProfile.Profile() if os.environ.get('AUDIT_PROFILE') else None
  def opened(file,mode='r',*a,**kw):
   if 'r' in mode:reads['n']+=1
   return orig(file,mode,*a,**kw)
  active['counts']={'file_read_open_events':0,'worker_selects':0}
  start=time.perf_counter()
  with perf.Probe(db,win.view if win else None) as q,mock.patch('builtins.open',opened):
   
   if profile:profile.enable()
   fn();settle()
   if profile:profile.disable()
  s=io.StringIO()
  if profile:pstats.Stats(profile,stream=s).sort_stats('tottime').print_stats(5)
  extra=active['counts'];active['counts']=None
  result={**extra,'size':n,'operation':label,'seconds':time.perf_counter()-start,'sql_selects_main_connection':q.selects,'sql_rows_main_connection':q.rows,'python_open_reads':reads['n'],'rss_mb':rss(),'peak_rss_mb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'draws':win.view.draws-draws,'view':perf.view_counts(win.view),'cpu_top':s.getvalue()};results.append(result);(out/f'map-complete-{n}.json').write_text(json.dumps(results,indent=2,default=str));print(n,label,round(result['seconds'],3),q.selects,flush=True)
 def start():
  global win
  win=MapWindow(root,db);win.geometry('1400x900');win.wait_for_startup(120)
  while win.view.draws<1:win.update()
 measure('open',start);v=win.view
 measure('pan regional',lambda:(v.ax.set_xlim(np.array(v.ax.get_xlim())+1000),v._view_changed()))
 measure('zoom regional',lambda:v.zoom_by(1.25))
 measure('field zoom',lambda:v.zoom_to((545000,4800000+(n//2000)*100-2000,549000,4800000+(n//2000)*100+2000),0))
 base=MP.well_settings(db)
 measure('apply labels field',lambda:win.apply_well_settings({**base,'size':7.0}))
 measure('symbol style field',lambda:win.apply_well_settings({**base,'symbol_size':11.0}))
 for k in range(4):measure(f'zoom repeat {k}',lambda k=k:v.zoom_by(0.8 if k%2 else 1.25))
 measure('rename grid',lambda:(setattr(win,'_selected_item',lambda:('grid',gid)),win.rename_layer('Renamed')))
 measure('rename image',lambda:(setattr(win,'_selected_item',lambda:('image',img.id)),win.rename_layer('Renamed Plat')))
 measure('grid visibility',lambda:(grids.set_visible(db,gid,False),win.refresh_grids()))
 measure('regional home',lambda:v.home())
 keys=[f"layer:{row['id']}" for row,layer in win.layers]
 measure('layer group create',lambda:(win.layer_list.selection_set(keys[0]),win.new_layer_group('Audit group')))
 group=win.layer_groups[-1]['id']
 measure('layer move into group',lambda:(win.layer_list.selection_set(keys[1]),win.move_to_group(group)))
 measure('layer order move',lambda:(win.layer_list.selection_set(keys[2]),win.move_layer(1)))
 measure('layer visibility',lambda:(setattr(win,'_selected_item',lambda:('shape',win.layers[0][0]['id'])),win.toggle_selected_layer()))
 measure('grid contours',lambda:(setattr(win,'_selected_item',lambda:('grid_part',(gid,'contours'))),win.toggle_selected_layer()))
 measure('raster opacity',lambda:win.set_image_opacity(img.id,0.45))
 xy=v._well_xy;cx,cy=np.median(xy,axis=0)
 measure('threshold setup 5000 wells',lambda:v.zoom_to((cx-2500,cy-5000,cx+2500,cy+5000),0))
 typ=type(v);real=typ.text_factor;real_records=typ._label_records;made={'n':0}
 def records(self,rows,grow):made['n']+=len(rows);return real_records(self,rows,grow)
 typ._label_records=records
 try:
  for k,f in enumerate([0.1,1.0,0.1,1.0,0.1,1.0]):
   typ.text_factor=lambda self,f=f:f;made['n']=0
   measure(f'threshold crossing {k} factor {f}',lambda:(v.refresh_wells(),v.redraw()))
   results[-1]['label_records_created']=made['n'];results[-1]['labels_drawn_paths']=sum(len(c.get_paths()) for c in v._well_label_collections)
  (out/f'map-complete-{n}.json').write_text(json.dumps(results,indent=2,default=str))
 finally:typ.text_factor=real;typ._label_records=real_records
 win.close();root.destroy();db.close()
