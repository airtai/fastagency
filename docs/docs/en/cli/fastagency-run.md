```

fastagency run [OPTIONS] [PATH]

```

Run a FastAgency app in production mode. 🚀                                    
 This is similar to the fastagency dev command, but optimized for production    
 environments.                                                                  
                                                                                
 It automatically detects the Python module or package that needs to be         
 imported based on the file or directory path passed.                           
                                                                                
 If no path is passed, it tries with:                                           
                                                                                
 - main.py                                                                      
 - app.py                                                                       
 - api.py                                                                       
 - app/main.py                                                                  
 - app/app.py                                                                   
 - app/api.py                                                                   
                                                                                
 It also detects the directory that needs to be added to the PYTHONPATH to make 
 the app importable and adds it.                                                
                                                                                
 It detects the FastAgency app object to use. By default it looks in the module 
 or package for an object named:                                                
                                                                                
 - app                                                                          
 - api                                                                          
                                                                                
 Otherwise, it uses the first FastAgency app found in the imported module or    
 package.


```

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│   path      [PATH]  A path to a Python file or package directory (with       │
│                     __init__.py files) containing a FastAgency app. If not   │
│                     provided, a default set of paths will be tried.          │
│                     [default: None]                                          │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --app                      TEXT  The name of the variable that contains the  │
│                                  app in the imported module or package. If   │
│                                  not provided, it is detected automatically. │
│                                  [default: None]                             │
│ --workflow         -w      TEXT  The name of the workflow to run. If not     │
│                                  provided, the default workflow will be run. │
│                                  [default: None]                             │
│ --initial_message  -i      TEXT  The initial message to send to the          │
│                                  workflow. If not provided, a default        │
│                                  message will be sent.                       │
│                                  [default: None]                             │
│ --help                           Show this message and exit.                 │
╰──────────────────────────────────────────────────────────────────────────────╯

```
