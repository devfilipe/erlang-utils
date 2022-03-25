ExtraDeps = [{cloudi_core, "{{cloudi_version}}"}].
CONFIG1 = case lists:keysearch(deps, 1, CONFIG) of
  {value, {deps, Deps}} ->
    NDeps = Deps ++ ExtraDeps,
    lists:keyreplace(deps, 1, CONFIG, {deps, NDeps});
  _ ->
    CONFIG ++ [{deps, ExtraDeps}]
end.
CONFIG1.
