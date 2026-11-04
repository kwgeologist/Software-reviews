exec(open('/workspace/audit-v0.9.4/probes/editor.py').read().split('out={}')[0])
out={}
with tempfile.TemporaryDirectory()as t:
 os.environ['OGW_SYMBOL_CATALOG']=str(Path(t)/'cat.json');C.install(C.builtin());root=tk.Tk();root.withdraw();d=SymbolCatalogDialog(root);d.load_form('GAS');d.v['code'].set('OIL')
 with patch('geoworkbench.symbol_catalog_dialog.messagebox.showerror'):accepted=d.apply_form()
 out={'duplicate_rename_accepted':accepted,'GAS_entry_restored':d.work.entry('GAS') is not None,'validation_after_rejection':d.work.validate(),'IHS_GAS_mapping_before_save':d.work.resolve_external_symbol('IHS','GAS').code};out['saved']=d.save();C._CURRENT=None;out['IHS_GAS_mapping_after_restart']=C.resolve_external_symbol('IHS','GAS').code;root.destroy()
C.install(C.builtin());(R.parent/'rename-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
