module Syntax

extend lang::std::Layout;

lexical Comment = @category="Comment" "//" ![\n]* !>> ![\n] $;

keyword Keywords
      = "model" | "Param" | "output" | "Connections" | "Agregator" | "components" | "True" | "False"
      | "connect" | "def" | "exchange" | "transformation" | "sensor" | "from"| "behaviour" | "UX"
      | "FIFO" | "LIFO" | "LVQ" | "PQ" 
      | "Global Variables"

      ;

lexical Id = @category="Variable" name_id: [a-zA-Z][a-zA-Z0-9_]* !>> [a-zA-Z0-9_] \Keywords;

lexical Natural = [0-9]+ !>> [0-9];

lexical Decimal = [0-9]+ "." [0-9]+ !>> [0-9];

lexical Comment = @lineComment @category="Comment" "#" ![\n]* $;


start syntax Application
      = ID name ComponentManager cm CommunicationManager? cmm ExecutionManager? em DeploymentManager? dm
      ;


syntax ComponentManager     
      = "Components" "{" Components+ components "}"
      ;

syntax CommunicationManager     
      = "Communication" "{" CommNods+ commnods Connection+ conn"}"
      ;


start syntax Program // model Connection connections Agregator agregator;
      = component: Component component
      | left phrases: Program l Program r
      ;

syntax Method
      = fifo: "FIFO"
      | lifo: "LIFO"
      | lvq : "LVQ"
      | pq : "PQ"
      ;

syntax Def
      = def: "def" ":" Id dest "." Id id "-\>" Id dest "." Id id
      // | part: Id id "from" Id dest
      ;

syntax Exchange
      = ex: "exchange" ":" Method method
      ;

syntax Transformation
      = tr: "transformation" ":" Behaviour
      ;

syntax Component 
      = model: Model m
      | sensor: Sensor s
      | ux: UX ux
      // | aggr: Agregator ag
      // | dup: Duplicator d
      // | swit: "switch" ":" Id sw InputOutputDecl* ios Behaviour // multiple inputs, 1 output
      // | splitter: "splitter" ":" Id sw InputOutputDecl* ios // 1 input, multiple outputs
      // | operation: "operation" ":" Id? sw2 InputOutputDecl* ios Behaviour //
      // | conn: "connect" ":" Id id Def Exchange e Transformation
      ;

syntax Model
      = model: "model" ":" Id modelName InputOutputDecl* ios
      ;

syntax Sensor
      = sensor: "sensor" ":" Id sensorName InputOutputDecl out 
      ;

syntax UX
      = ux: "UX" ":" Id ux InputOutputDecl+ ios
      ;

syntax Agregator
      = agg: "aggregator" ":" Id agg InputOutputDecl* ios // multiple inputs, 1 output
      ;

syntax Duplicator
      = dup: "duplicator" ":" Id dup InputOutputDecl* ios // 1 input, multiple outputs 
      ;

// In the end, this are statements(?)
syntax Behaviour
      = behav: "behaviour" ":" Behaviour+ b
      | loop: "while" Expression e ":" Behaviour s
      | cond: "if" Expression e ":" Behaviour s "else" ":" Behaviour ss
      | assign: Id id "=" Expression e  
      ;

syntax ExpressionList
      = args: {Expression ","}+ args
      ;

syntax Expression
      = dot: Expression a "." Id id "(" Expression? opt ")"
      // | bracket "(" Expression x ")"
      | funcCall: Id "(" ExpressionList params ")"
      | subscrpt: "[" {Expression ","}* "]"
      | name: Id id Expression e
      | ids: Id lid ":" Id rid
      | id: Id id
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
      ;

syntax LiteralExpression
      = nat: Natural i 
      | fl: Decimal f
      ;

syntax InputOutputDecl
      = input: "input" ":" InputOutputDecl
      | output: "output" ":" InputOutputDecl
      | units: Typ typ Id enum "[" {Unit ","}+ "]" "components" ":" "[" {Expression ","}+ comps "]"
      | units2: Typ typ Id enum "[" {Unit ","}+ "]"
      | units3: Id enum "[" {Unit ","}+ "]"
      ;

syntax Typ
      = float: "float"
      | string: "str"
      | dict: "dict" //dict(str, str)
      | lst: "list" //list(str, str)
      ;

syntax Unit
      = k: "K"
      | k2: "Kelvin"
      | c: "Celcius"
      | c2: "°C"
      | f: "Fahrenheit"
      | f2: "°F"
      | meter: "Meter"
      | gl: "g/l"
      | mol_l: "mol/l"
      | mol_s: "mol/l_s"
      ;
