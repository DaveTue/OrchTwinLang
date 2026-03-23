module LOTTS

extend lang:: std:: Layout;

lexical Comment = @category="Comment" "//" ![\n]* !>> ![\n] $;

keyword Keywords
      = "model" | "sensor" | "actuator" | "ux" | "db"| "dataprocess" | "global"
      | "config" | "def"
      | "agregator" | "switch" | "duplicate" | "splitter" | "transformation" | "connect"    
      | "FIFO" | "LIFO" | "LVQ" | "PQ" 
      | "source" | "sink"| "trigger" |"cosim"
      |"event" |"temporal" |"guard" | "data"
      |"freq" |"time_elapse"
      |"streaming" |"time_specific" |"invoke"
      |"continuous" |"time-based" |"scheduling"
      |"t_ini"|"t_step"|"t_period"
      |"eval"|"comp"|"values"
      ;

lexical Id = @category="Variable" name_id: [a-zA-Z][a-zA-Z0-9_]* !>> [a-zA-Z0-9_] \Keywords;

lexical Natural = [0-9]+ !>> [0-9];

lexical Decimal = [0-9]+ "." [0-9]+ !>> [0-9];

lexical Comment = @lineComment @category="Comment" "#" ![\n]* $;

layout NoNewLineLayout = @manual [\t\ ]*;

start syntax Application
      = Id name ComponentManager cm //CommunicationManager? cmm //ExecutionManager? em DeploymentManager? dm
      ;

// Managers definition
syntax ComponentManager     
      = "Component manager:"  Component+ component
      ;

// syntax CommunicationManager     
//       = "Communication" "{" CommNods+ commnods Connection+ conn"}"
//       ;

//component manager grammar definition

syntax Component
      = sensor: Sensor s 
      | actuator: Actuator a
      | ux: UX u
      | bd: DB b 
      | model: Model m
      | dataprocess: Dataprocess dp 
      | global: Global g 
      ;

syntax Port
      = input: "(" Typ typ ")" Port "(" Unit unit ")"
      | output: "(" Typ typ ")" Port "(" Unit unit ")"
      //| how to define complex inputs outputs? (float,float) [temp,mass] (K,kg)
      ;

syntax Sensor
      = sensor: "sensor"  Id sensorName " -\> " "[" {Port out ","}* "]"
      ;

syntax Actuator
      = actuator: "actuator"  Id actuatorName "(" {Port in ","}* ")""-\>" "None"
      ;

syntax UX
      = ux: "ux"  Id uxname "(" {Port in ","}* ")""-\>" "[" {Port out ","}* "]"
      ;

syntax DB
      = db: "db"  Id dbname "(" {Port in ","}* ")""-\>" "[" {Port out ","}* "]"
      ;

syntax Dataprocess
      = dataprocess: "dataprocess"  Id datapname "(" {Port in ","}* ")""-\>" "[" {Port out ","}* "]"
      ;

syntax Model
      = model: "model"  Id modelname "(" {Port in ","}* ")""-\>" "[" {Port out ","}* "]:" ModelConfiguration?
      ;

syntax ModelConfiguration //some questions here: how to make the ports in the parenthesis optional?
      = configuration: "config" "(" {Port in ","}* ")" ":" Expression //Always need to be an assigment expression
      ;

syntax Global
      = global: "global"  "(" {Port ","}* in ")""-\>" "None:" Expression //Always need to be an assigment expression
      ;


//language definition that are more general

syntax Typ
      = float: "float"
      | string: "str"
      | json : "JSON"
      | integer: "int"
      
      |complex: "[" {Typ ","}+ "]"
      
      // | dict: "dict" //dict(str, str)
      // | lst: "list" //list(str, str)
      ;

// syntax Unit
//       = k: "K"
//       | k2: "Kelvin"
//       | c: "Celcius"
//       | c2: "°C"
//       | f: "Fahrenheit"
//       | f2: "°F"
//       | meter: "Meter"
//       | gl: "g/l"
//       | mol_l: "mol/l"
//       | mol_s: "mol/l_s"
//       ;

syntax Unit
      = derived: BasicUnit "-" !>> Natural
      |complex: "[" {Unit ","}+ u "]" // how to fix this one?
      ;

syntax BasicUnit
      =second: "s" //time
      |meter: "m" //length
      |kilogram:"kg" //mass
      |ampere:"A" // electric current
      |kelvin: "K" // thermodynamic temperature
      |mole: "mol" //amount of substance
      |candela:"cd" // luminous intensity
      | non: "-"
      ;
syntax Expression
      = assign: Id id "=" Expression e
      | loop: "while" Expression e ":" Expression s
      | cond: "if" Expression e ":" Expression s "else" ":" Expression ss
;