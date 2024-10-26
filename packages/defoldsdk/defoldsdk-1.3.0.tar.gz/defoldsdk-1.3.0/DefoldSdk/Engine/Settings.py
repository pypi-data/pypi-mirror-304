





class Settings : 
    SavingPolicy  = dict(
        EmbeddedInstanceDesc = "Gameobjects" , 
        Atlas = 'Atlases' , 
        MaterialDesc  = 'Materials/{name}' , 
        CollectionDesc = 'Collections'
    )
    FileNamingPolicy  = dict(
        CollectionDesc = '{name}.collection'
    )
    Templates = "https://github.com/MhadhbiXissam/defold-templates"
    defaultTemplate = "default"
