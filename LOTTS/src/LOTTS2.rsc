module LOTTS2

extend lang:: std:: Layout;

layout NEW_LINE = @manual [\r\n]*[\ ]+
                | @manual [\ ]*[\r\n]*[\ ]+;
lexical Comment = @category="Comment" "//" ![\n]* !>> ![\n] $;
lexical Comment = @lineComment @category="Comment" "#" ![\n]* $;

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

lexical Id = @category="Variable" name_id: [a-zA-Z][a-zA-Z0-9_\-]* !>> [a-zA-Z0-9_] \Keywords;

lexical Natural = [0-9]+ !>> [0-9];

lexical Decimal = [0-9]+ "." [0-9]+ !>> [0-9];

start syntax Service
      = compmng:"Service Name" ":" Id name ComponentManager cm //CommunicationManager? cmm  ExecutionManager?  em // DeploymentManager? dm [\r\n]*
      | commmng: "Service Name" ":" Id name ComponentManager cm CommunicationManager cmm  //ExecutionManager?  em // DeploymentManager? dm [\r\n]*
      | exemng: "Service Name" ":" Id name ComponentManager cm CommunicationManager cmm  ExecutionManager  em // DeploymentManager? dm [\r\n]*
      ;

// Component Managers definition
syntax ComponentManager     
      = "Component_manager:" Component+ component
      ;
syntax Component
      = sensor: Sensor s 
      | actuator: Actuator a
      | ux: UX u
      | bd: DB b 
      | model: Model m
      | dataprocess: Dataprocess dp 
      | global: Global g 
      ;

syntax Ports
    = "ports" ":" NEW_LINE Port;

syntax Port
      = "(" Typ typ ")" Id name "(" Unit+ units ")"
      //| output: "(" Typ typ ")" Id "(" Unit unit ")"
      //| how to define complex inputs outputs? (float,float) [temp,mass] (K,kg)
      ;

syntax PortList
    // ="[" Port out"]"
     = {Port ","}* ports 
    ;

syntax Sensor
     //  = "sensor"  Id sensorName "-\>" "[" Port out"]"
     = "sensor"  Id name "-\>" "[" {Port ","}+ outs  "]"
    ;

syntax Actuator
      = actuator: "actuator"  Id name "(" {Port ","}* ins ")" "-\>" "None"
    //   |actuator: "actuator"  Id actuatorName "(" PortList ins ")" "-\>" "None"
      ;

syntax UX
      = bothports: "ux"  Id name "("  {Port ","}* ins ")""-\>" "[" {Port ","}* outs "]"
      | onlyouts: "ux"  Id name "-\>" "[" {Port ","}* outs "]"
      | onlyins: "ux"  Id name "("  {Port ","}* ins ")""-\>" "None"
      ;

syntax DB
      =  bothports:"db"  Id name "(" {Port ","}* ins ")""-\>" "[" {Port ","}* outs "]"
      |  onlyouts: "db"  Id name "-\>" "[" {Port ","}* outs "]"
      |  onlyins: "db"  Id name "("  {Port ","}* ins ")""-\>" "None"
      ;

syntax Dataprocess
      = dataprocess: "dataprocess"  Id name "(" {Port ","}* ins ")""-\>" "[" {Port ","}* outs "]"
      ;


syntax Global
      = "global"  "(" {Port ","}* ins ")""-\>" "None" 
      | "global"  "(" {Port ","}* ins ")""-\>" "None:" EspecialExp+ //Always need to be an assigment expression
      | "global"  "-\>" "None:" EspecialExp+ //Always need to be an assigment expression 
      ;

syntax Model
      = "model"  Id name "(" {Port ","}* ins ")""-\>" "[" {Port ","}* outs "]"
       |  "model"  Id name "(" {Port ","}* ins ")""-\>" "[" {Port ","}* outs "]" ":" NEW_LINE ModelConfiguration
      ;

syntax ModelConfiguration //some questions here: how to make the ports in the parenthesis optional?
      = "config" ":" NEW_LINE EspecialExp+ //Always need to be an assigment expression
      | "config" "(" {Port ","}* ins ")"  //Always need to be an assigment expression
      | "config" "(" {Port ","}* ins ")" ":" NEW_LINE EspecialExp+ //Always need to be an assigment expression
      ;


// Communication Manager def
syntax CommunicationManager     
      = "Communication_manager:" CommComp+ commcomp
      // = "Communication_manager:" NEW_LINE CommComp+ commcomp [\r\n]*
      ;
syntax CommComp
      = swit: Switch sw 
      | duplicator: Duplicator du
      | splitter: Splitter split
      | aggregator: Aggregator agg
      | transformation: Transformation transf
      | connector: Connector connect
      ;

syntax Duplicator
      = "duplicate"  Id name "(" Port ins ")""-\>" "[" {Port ","}* outs "]"
      ;

syntax Splitter
      =  "split"  Id name "(" Port ins ")""-\>" "[" {Port ","}* outs "]"
      ;

syntax Aggregator
      =  "aggregate"  Id name "(" {Port ","}* ins ")""-\>" "[" Port outs "]"
      ;

syntax Switch
      = "switch"  Id name "(" {Port ","}* ins ")""-\>" "[" Port outs "]:" NEW_LINE "def:" NEW_LINE EspecialExp exp
      // ="switch"  Id switname "(" {Port ","}* ins ")""-\>" "[" Port out "]" NEW_LINE "def:" 
    //   | "switch"  Id switname "(" {Port ","}* ins ")""-\>" "[" {Port ","}* ins "]" NEW_LINE "def:" NEW_LINE Expression
      ;

syntax Transformation
      // = "transform"  Id transfname "(" {Port ","}* ins ")""-\>" "[" {Port ","}* ins "]:" NEW_LINE "def:" NEW_LINE EspecialExp
      ="transform"  Id name "(" {Port ","}* ins ")""-\>" "[" {Port ","}* outs "]:" NEW_LINE "def:" NEW_LINE Expression+
      // = "transform"  Id transfname "(" {Port ","}* ins ")""-\>" "[" {Port ","}* outs "]:" NEW_LINE "def:"

      ;

syntax Connector
    = "connect" Id name "(" "src:"? Id src_comp "." Id out_port "," "dst:"? Id dst_comp "." Id in_port ")" "-\>" ExchMethod
    ;

syntax ExchMethod
      = fifo: "FIFO"
      | lifo: "LIFO"
      | lvq : "LVQ"
      | pq : "PQ"
      ;

// ExecutionManager Manager def
syntax ExecutionManager     
      = "Execution_manager:" ExecComp+ execcomp [\r\n]*
      ;
syntax ExecComp
      = srcexe: SrcExe srcexe
      | sinkexe: SinkExe sinkexe
      | cosimexe: CoSimExe cosimexe
      ;

syntax SrcExe
      = "source" Id name "(" {Id ","}+ srcComp")" "-\>" ExecType ":" NEW_LINE Trigger tr
      | "source" Id name "(" {Id ","}+ srcComp")" "-\>" ExecType ":" NEW_LINE Trigger tr NEW_LINE "def:" NEW_LINE? TempDef // this one only applies for time_specific
      ;

syntax SinkExe    
      = "sink" Id name "(" {Id ","}+ sinkComp")" "-\>" ExecType ":" NEW_LINE Trigger 
      | "sink" Id name "(" {Id ","}+ sinkComp")" "-\>" ExecType ":" NEW_LINE Trigger NEW_LINE "def:" NEW_LINE? TempDef // this one only applies for time_specific
      ;
// syntax SrcComp
//       = srcarea: SrcExe
//       | sensor: Sensor s 
//       | ux: UX u
//       | bd: DB b 
//       | dataprocess: Dataprocess dp 
//       ;

syntax CoSimExe   
      = "cosim" Id name "(" {Id ","}+ cosimComp")" "-\>" "invoke" ":" NEW_LINE Trigger 
      | "cosim" Id name "(" {Id ","}+ cosimComp")" "-\>" "scheduling" ":" NEW_LINE Trigger NEW_LINE "def:" NEW_LINE? Expression* ex Eval* ev
      | "cosim" Id name "(" {Id ","}+ cosimComp")" "-\>" "continuous" ":" NEW_LINE Trigger NEW_LINE "def:" NEW_LINE? TempDef //this is not well defined
      | "cosim" Id name "(" {Id ","}+ cosimComp")" "-\>" "time_based" ":" NEW_LINE Trigger NEW_LINE TimeBasedConfig
      ;

syntax ExecType
      = streaming: "streaming"
      | time: "time_specific"
      | invoke: "invoke"
      ;
// syntax SimType
//       = invoke: "invoke"
//       | cont:"continuous"
//       | time_based: "time_based"
//       | schedule:"scheduling"
//       ;

syntax TimeBasedConfig
      = "config:" NEW_LINE "exe_time" "=" SimTime NEW_LINE "t_ini" "=" Expression NEW_LINE "t_step" "=" Natural "(" TimeUnit ")"  NEW_LINE "t_period" "=" Natural "(" TimeUnit ")"  
      ;
syntax Trigger
      
      =guard: "trigger" "-\>" "guard" "." Trigger_type ":" NEW_LINE Expression e// only accept expression of comp, l, lt, h, ht
      |temporal: "trigger" "-\>" "temporal" "." Trigger_type ":" NEW_LINE TempDef tdef
      |signal: "trigger" "-\>" "signal" "." Trigger_type ":" NEW_LINE Id connectorName // only accept connectors, since connectors contains signals     
      |event: "trigger" "-\>" "event" "." Trigger_type ":" NEW_LINE?  {Triggerdef LogicalOp}+ 
      ;



// triggers definitions
syntax Trigger_type
      = "start"| "stop"
      ;

syntax Triggerdef
      = Expression // only accept expression of comp, l, lt, h, ht
      |TempDef
      |Id // only accept connectors, since connectors contains signals     
      ;

syntax TempDef
      = frequency: "freq" "=" Natural "(" TimeUnit")"
      | relative: "time_elapse" "=" Natural "(" TimeUnit ")"  
      // | absolute: "clock"   [1-9]|1[012] "hr" // how to define a clock grammar
      ;

syntax SimTime
      = "RT"|"FTRT" // name convention: https://dl.acm.org/doi/10.1145/3470481.3472703
      ;
// syntax Trigger_class
//       = eve:"event"
//       | temp: "temporal"
//       | guard: "guard"
//       | signal:"signal"

      // ;

//General used
syntax Typ
      = float: "float"
      | string: "str"
      | json : "JSON"
      | integer: "int"
      | boolean: "bool"     
      |frame: "frame" 
      | complex: "[" {Typ ","}+ "]"
      
      // | dict: "dict" //dict(str, str)
      // | lst: "list" //list(str, str)
      ;

syntax Unit //some ambiguities in this defition
      = basic_unit: BasicUnit+ basicUnits
      |power_neg_num: BasicUnit "^" "-" Natural
      |power_pos_num: BasicUnit basicUnit "^"Natural
      |derive: Unit+ units
      |complex: "[" {Unit ","}+ u "]" // how to fix this one?
      ;
syntax TimeUnit
      = hr:"hr"
      | min:"min"
      | sec: "s"
      | milisec: "ms"
      ;

syntax BasicUnit
      =second: "s" //time
      |meter: "m" //length
      |kilogram:"kg" //mass
      |ampere:"A" // electric current
      |kelvin: "K" // thermodynamic temperature
      |celsious: "C"
      |mole: "mol" //amount of substance
      |candela:"cd" // luminous intensity
      |mililiter :"ml" //volume
      |kilometer: "km" //distance very used
      |hour: "hr" //time hour
      |newton: "N" //force
      |joule:"J"
      |grams: "g"
      | non: "-"
      ;
syntax ExpressionList
      = args: {Expression ","}+ args
      ;
syntax EspecialExp
    = assign: Id id "=" LiteralExpression le "(" Unit u ")"
      | loop: "while" Expression e ":" Expression s
      | cond: "if" Expression e ":" Expression s "else" ":" Expression ss
    ;

syntax LogicalOp
      = "AND"
      |"OR"
      ;
syntax Expression
      =dot: Expression a "." Id id "(" Expression? opt ")"
      | component: Expression a "." Id id //ambigous with dot expression, but necessary for calling values in components
      | funcCall: Id "(" ExpressionList params ")"
      | subscrpt: "[" {Expression ","}* "]"
      | name: Id id Expression e // ambiguity with dot expression
      | ids: Id lid ":" Id rid
      | id: Id id
      | complex_data : Id "[" Natural"]"
      | literals: LiteralExpression
      > left comp: Expression l "==" Expression r
      > left div: Expression l "/" Expression r
      > left mul: Expression l  "*" Expression r
      > left add: Expression l "+" Expression r
      > left min: Expression l "-" Expression r
      > left lt: Expression l "\<" Expression r
      > left lte: Expression l "\<=" Expression r
      > left gt: Expression l "\>" Expression r
      > left gte: Expression l "\>=" Expression r
      > left assign:Expression l "=" Expression r    
      ;
syntax Eval
      = "[" {Id ","}* outnames "]" "=" "eval" "(" "components" "=" "[" {Id ","}* modelNames "]" "," "vars_assigment" "=" "[" {Expression ","}* inputsAssigVal  "]" ")"
      ;

// syntax AssignVal //how to make it more general
//       = Id "=" LiteralExpression
      // ;
syntax LiteralExpression
      = nat: Natural i 
      | fl: Decimal f
      ;