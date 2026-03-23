Blockly.Blocks['Typ/frame'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Typ/frame",
			  "message0" : "frame",
			  
			  "colour" : 70,
			  
			  "previousStatement" : "Typ",
			  "nextStatement" : "Typ",
			  "inputsInline" : true,
			  "tooltip" : "frame",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Aggregator/aggr'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Aggregator/aggr",
			  "message0" : "aggregate %1 %2 ( %3 ) %4 -> %5 [ %6 %7 ] %8 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Port",
				  "type" : "input_statement",
				  "check" : ["Port"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 79,
			  "output" : "Aggregator",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "aggr",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/candela'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/candela",
			  "message0" : "cd",
			  
			  "colour" : 131,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "candela",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/complex_data'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/complex_data",
			  "message0" : "%1 [ %2 %3 ] %4 ",
			  "args0" : [
				{
				  "name" : "lex",
				  "type" : "field_input",
				  "text" : "Expression"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "lex",
				  "type" : "input_value",
				  "check" : ["Natural"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 337,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "complex_data",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['TimeUnit/min'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "TimeUnit/min",
			  "message0" : "min",
			  
			  "colour" : 218,
			  "output" : "TimeUnit",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "min",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['CoSimExe/c4'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "CoSimExe/c4",
			  "message0" : "cosim %1 %2 ( %3 ) %4 -> %5 time_based %6 : %7 %8 %9 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Trigger",
				  "type" : "input_value",
				  "check" : ["Trigger"]
				},
				  	{
				  "name" : "TimeBasedConfig",
				  "type" : "input_value",
				  "check" : ["TimeBasedConfig"]
				},
				
			],
			  "colour" : 82,
			  "output" : "CoSimExe",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "c4",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['LogicalOp/or'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "LogicalOp/or",
			  "message0" : "OR",
			  
			  "colour" : 181,
			  
			  "previousStatement" : "LogicalOp",
			  "nextStatement" : "LogicalOp",
			  "inputsInline" : true,
			  "tooltip" : "or",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ExchMethod/fifo'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ExchMethod/fifo",
			  "message0" : "FIFO",
			  
			  "colour" : 51,
			  "output" : "ExchMethod",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "fifo",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['EspecialExp/assign'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "EspecialExp/assign",
			  "message0" : "%1 = %2 %3 ( %4 %5 ) %6 ",
			  "args0" : [
				{
				  "name" : "id",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "LiteralExpression",
				  "type" : "input_value",
				  "check" : ["LiteralExpression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Unit",
				  "type" : "input_statement",
				  "check" : ["Unit"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 121,
			  
			  "previousStatement" : "EspecialExp",
			  "nextStatement" : "EspecialExp",
			  "inputsInline" : true,
			  "tooltip" : "assign",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Global/g1'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Global/g1",
			  "message0" : "global %1 ( %2 ) %3 -> %4 None %5 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 53,
			  "output" : "Global",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "g1",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Trigger/signal'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Trigger/signal",
			  "message0" : "trigger %1 -> %2 signal %3 . %4 %5 : %6 %7 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Trigger_type",
				  "type" : "input_value",
				  "check" : ["Trigger_type"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "connectorName",
				  "type" : "field_input",
				  "text" : ""
				},
				
			],
			  "colour" : 316,
			  "output" : "Trigger",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "signal",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/mililiter'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/mililiter",
			  "message0" : "ml",
			  
			  "colour" : 291,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "mililiter",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['CommComp/swit'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "CommComp/swit",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "Switch",
				  "type" : "input_value",
				  "check" : ["Switch"]
				},
				
			],
			  "colour" : 104,
			  
			  "previousStatement" : "CommComp",
			  "nextStatement" : "CommComp",
			  "inputsInline" : true,
			  "tooltip" : "swit",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['UX/onlyins'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "UX/onlyins",
			  "message0" : "ux %1 %2 ( %3 ) %4 -> %5 None %6 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 90,
			  "output" : "UX",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "onlyins",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Switch/swt'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Switch/swt",
			  "message0" : "switch %1 %2 ( %3 ) %4 -> %5 [ %6 %7 ]: %8 def: %9 %10 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Port",
				  "type" : "input_statement",
				  "check" : ["Port"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "EspecialExp",
				  "type" : "input_statement",
				  "check" : ["EspecialExp"]
				},
				
			],
			  "colour" : 253,
			  "output" : "Switch",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "swt",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/name'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/name",
			  "message0" : "%1 %2 ",
			  "args0" : [
				{
				  "name" : "id",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 257,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "name",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ExpressionList/args'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ExpressionList/args",
			  "message0" : "",
			  
			  "colour" : 36,
			  "output" : "ExpressionList",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "args",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['DB/bothports'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "DB/bothports",
			  "message0" : "db %1 %2 ( %3 ) %4 -> %5 [ %6 ] %7 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 341,
			  "output" : "DB",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "bothports",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Typ/integer'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Typ/integer",
			  "message0" : "int",
			  
			  "colour" : 320,
			  
			  "previousStatement" : "Typ",
			  "nextStatement" : "Typ",
			  "inputsInline" : true,
			  "tooltip" : "integer",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['TimeUnit/hr'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "TimeUnit/hr",
			  "message0" : "hr",
			  
			  "colour" : 312,
			  "output" : "TimeUnit",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "hr",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['SimTime/ft'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "SimTime/ft",
			  "message0" : "FTRT",
			  
			  "colour" : 204,
			  "output" : "SimTime",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "ft",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Service/exemng'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Service/exemng",
			  "message0" : "Service Name %1 : %2 %3 %4 %5 %6 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "ComponentManager",
				  "type" : "input_value",
				  "check" : ["ComponentManager"]
				},
				  	{
				  "name" : "CommunicationManager",
				  "type" : "input_value",
				  "check" : ["CommunicationManager"]
				},
				  	{
				  "name" : "ExecutionManager",
				  "type" : "input_value",
				  "check" : ["ExecutionManager"]
				},
				
			],
			  "colour" : 120,
			  
			  
			  
			  "inputsInline" : false,
			  "tooltip" : "",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['CommComp/duplicator'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "CommComp/duplicator",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "Duplicator",
				  "type" : "input_value",
				  "check" : ["Duplicator"]
				},
				
			],
			  "colour" : 133,
			  
			  "previousStatement" : "CommComp",
			  "nextStatement" : "CommComp",
			  "inputsInline" : true,
			  "tooltip" : "duplicator",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['TimeBasedConfig/tb'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "TimeBasedConfig/tb",
			  "message0" : "config: %1 exe_time %2 = %3 %4 t_ini %5 = %6 %7 t_step %8 = %9 %10 ( %11 %12 ) %13 t_period %14 = %15 %16 ( %17 %18 ) %19 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "SimTime",
				  "type" : "input_value",
				  "check" : ["SimTime"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "lex",
				  "type" : "input_value",
				  "check" : ["Natural"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "TimeUnit",
				  "type" : "input_value",
				  "check" : ["TimeUnit"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "lex",
				  "type" : "input_value",
				  "check" : ["Natural"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "TimeUnit",
				  "type" : "input_value",
				  "check" : ["TimeUnit"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 292,
			  "output" : "TimeBasedConfig",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "tb",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/literals'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/literals",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "LiteralExpression",
				  "type" : "input_value",
				  "check" : ["LiteralExpression"]
				},
				
			],
			  "colour" : 220,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "literals",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/add'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/add",
			  "message0" : "%1 + %2 %3 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 103,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "add",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Component/dataprocess'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Component/dataprocess",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "Dataprocess",
				  "type" : "input_value",
				  "check" : ["Dataprocess"]
				},
				
			],
			  "colour" : 172,
			  
			  "previousStatement" : "Component",
			  "nextStatement" : "Component",
			  "inputsInline" : true,
			  "tooltip" : "dataprocess",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Typ/string'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Typ/string",
			  "message0" : "str",
			  
			  "colour" : 186,
			  
			  "previousStatement" : "Typ",
			  "nextStatement" : "Typ",
			  "inputsInline" : true,
			  "tooltip" : "string",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Trigger/temporal'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Trigger/temporal",
			  "message0" : "trigger %1 -> %2 temporal %3 . %4 %5 : %6 %7 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Trigger_type",
				  "type" : "input_value",
				  "check" : ["Trigger_type"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "TempDef",
				  "type" : "input_value",
				  "check" : ["TempDef"]
				},
				
			],
			  "colour" : 89,
			  "output" : "Trigger",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "temporal",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Service/compmng'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Service/compmng",
			  "message0" : "Service Name %1 : %2 %3 %4 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "ComponentManager",
				  "type" : "input_value",
				  "check" : ["ComponentManager"]
				},
				
			],
			  "colour" : 120,
			  
			  
			  
			  "inputsInline" : false,
			  "tooltip" : "",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ModelConfiguration/always'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ModelConfiguration/always",
			  "message0" : "config %1 : %2 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 4,
			  "output" : "ModelConfiguration",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "always",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Component/sensor'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Component/sensor",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "Sensor",
				  "type" : "input_value",
				  "check" : ["Sensor"]
				},
				
			],
			  "colour" : 317,
			  
			  "previousStatement" : "Component",
			  "nextStatement" : "Component",
			  "inputsInline" : true,
			  "tooltip" : "sensor",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ModelConfiguration/mc3'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ModelConfiguration/mc3",
			  "message0" : "config %1 ( %2 ) %3 : %4 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 9,
			  "output" : "ModelConfiguration",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "mc3",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Id/name_id'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Id/name_id",
			  "message0" : "%1",
			  "args0" : [
				{
				  "name" : "Id",
				  "type" : "field_input",
				  "text" : "variable"
				},
				
			],
			  "colour" : 233,
			  
			  "previousStatement" : "Id",
			  "nextStatement" : "Id",
			  "inputsInline" : true,
			  "tooltip" : "",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['SinkExe/sn'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "SinkExe/sn",
			  "message0" : "sink %1 %2 ( %3 ) %4 -> %5 %6 : %7 %8 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "ExecType",
				  "type" : "input_value",
				  "check" : ["ExecType"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Trigger",
				  "type" : "input_value",
				  "check" : ["Trigger"]
				},
				
			],
			  "colour" : 336,
			  "output" : "SinkExe",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "sn",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/id'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/id",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "id",
				  "type" : "field_input",
				  "text" : ""
				},
				
			],
			  "colour" : 217,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "id",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/kilometer'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/kilometer",
			  "message0" : "km",
			  
			  "colour" : 104,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "kilometer",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/mole'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/mole",
			  "message0" : "mol",
			  
			  "colour" : 146,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "mole",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/mul'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/mul",
			  "message0" : "%1 * %2 %3 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 273,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "mul",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['TempDef/relative'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "TempDef/relative",
			  "message0" : "time_elapse %1 = %2 %3 ( %4 %5 ) %6 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "lex",
				  "type" : "input_value",
				  "check" : ["Natural"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "TimeUnit",
				  "type" : "input_value",
				  "check" : ["TimeUnit"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 350,
			  "output" : "TempDef",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "relative",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Global/g3'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Global/g3",
			  "message0" : "global %1 -> %2 None: %3 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 219,
			  "output" : "Global",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "g3",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Splitter/spl'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Splitter/spl",
			  "message0" : "split %1 %2 ( %3 %4 ) %5 -> %6 [ %7 ] %8 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Port",
				  "type" : "input_statement",
				  "check" : ["Port"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 354,
			  "output" : "Splitter",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "spl",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Ports'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Ports",
			  "message0" : "ports %1 : %2 %3 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Port",
				  "type" : "input_statement",
				  "check" : ["Port"]
				},
				
			],
			  "colour" : 85,
			  
			  "previousStatement" : "Ports",
			  "nextStatement" : "Ports",
			  "inputsInline" : true,
			  "tooltip" : "",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/gte'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/gte",
			  "message0" : "%1 >= %2 %3 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 181,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "gte",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/lt'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/lt",
			  "message0" : "%1 < %2 %3 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 151,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "lt",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Global/g2'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Global/g2",
			  "message0" : "global %1 ( %2 ) %3 -> %4 None: %5 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 343,
			  "output" : "Global",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "g2",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Typ/complex'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Typ/complex",
			  "message0" : "[ %1 ] %2 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 126,
			  
			  "previousStatement" : "Typ",
			  "nextStatement" : "Typ",
			  "inputsInline" : true,
			  "tooltip" : "complex",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['LiteralExpression/nat'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "LiteralExpression/nat",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "i",
				  "type" : "input_value",
				  "check" : ["Natural"]
				},
				
			],
			  "colour" : 124,
			  "output" : "LiteralExpression",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "nat",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/hour'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/hour",
			  "message0" : "hr",
			  
			  "colour" : 95,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "hour",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Triggerdef/te'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Triggerdef/te",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 336,
			  
			  "previousStatement" : "Triggerdef",
			  "nextStatement" : "Triggerdef",
			  "inputsInline" : true,
			  "tooltip" : "te",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Component/global'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Component/global",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "Global",
				  "type" : "input_value",
				  "check" : ["Global"]
				},
				
			],
			  "colour" : 306,
			  
			  "previousStatement" : "Component",
			  "nextStatement" : "Component",
			  "inputsInline" : true,
			  "tooltip" : "global",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['LiteralExpression/fl'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "LiteralExpression/fl",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "f",
				  "type" : "input_value",
				  "check" : ["Decimal"]
				},
				
			],
			  "colour" : 273,
			  "output" : "LiteralExpression",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "fl",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/non'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/non",
			  "message0" : "-",
			  
			  "colour" : 89,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "non",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Model/m2'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Model/m2",
			  "message0" : "model %1 %2 ( %3 ) %4 -> %5 [ %6 ] %7 : %8 %9 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "ModelConfiguration",
				  "type" : "input_value",
				  "check" : ["ModelConfiguration"]
				},
				
			],
			  "colour" : 267,
			  "output" : "Model",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "m2",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/lte'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/lte",
			  "message0" : "%1 <= %2 %3 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 325,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "lte",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/celsious'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/celsious",
			  "message0" : "C",
			  
			  "colour" : 102,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "celsious",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/subscrpt'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/subscrpt",
			  "message0" : "[ %1 ] %2 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 127,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "subscrpt",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['DB/onlyouts'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "DB/onlyouts",
			  "message0" : "db %1 %2 -> %3 [ %4 ] %5 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 321,
			  "output" : "DB",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "onlyouts",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Component/actuator'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Component/actuator",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "Actuator",
				  "type" : "input_value",
				  "check" : ["Actuator"]
				},
				
			],
			  "colour" : 94,
			  
			  "previousStatement" : "Component",
			  "nextStatement" : "Component",
			  "inputsInline" : true,
			  "tooltip" : "actuator",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Port/port'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Port/port",
			  "message0" : "( %1 %2 ) %3 %4 ( %5 ) %6 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Typ",
				  "type" : "input_statement",
				  "check" : ["Typ"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 43,
			  
			  "previousStatement" : "Port",
			  "nextStatement" : "Port",
			  "inputsInline" : true,
			  "tooltip" : "port",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Trigger/guard'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Trigger/guard",
			  "message0" : "trigger %1 -> %2 guard %3 . %4 %5 : %6 %7 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Trigger_type",
				  "type" : "input_value",
				  "check" : ["Trigger_type"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 241,
			  "output" : "Trigger",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "guard",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Trigger_type/t'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Trigger_type/t",
			  "message0" : "start",
			  
			  "colour" : 179,
			  "output" : "Trigger_type",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "t",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Unit/derive'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Unit/derive",
			  "message0" : "",
			  
			  "colour" : 340,
			  
			  "previousStatement" : "Unit",
			  "nextStatement" : "Unit",
			  "inputsInline" : true,
			  "tooltip" : "derive",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Natural'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Natural",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "NaturalName",
				  "type" : "field_number",
				  "value" : 0
				},
				
			],
			  "colour" : 57,
			  "output" : "Natural",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ExchMethod/lvq'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ExchMethod/lvq",
			  "message0" : "LVQ",
			  
			  "colour" : 222,
			  "output" : "ExchMethod",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "lvq",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Unit/power_neg_num'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Unit/power_neg_num",
			  "message0" : "%1 ^ %2 - %3 %4 ",
			  "args0" : [
				{
				  "name" : "BasicUnit",
				  "type" : "input_statement",
				  "check" : ["BasicUnit"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "lex",
				  "type" : "input_value",
				  "check" : ["Natural"]
				},
				
			],
			  "colour" : 14,
			  
			  "previousStatement" : "Unit",
			  "nextStatement" : "Unit",
			  "inputsInline" : true,
			  "tooltip" : "power_neg_num",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Typ/json'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Typ/json",
			  "message0" : "JSON",
			  
			  "colour" : 70,
			  
			  "previousStatement" : "Typ",
			  "nextStatement" : "Typ",
			  "inputsInline" : true,
			  "tooltip" : "json",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Model/m1'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Model/m1",
			  "message0" : "model %1 %2 ( %3 ) %4 -> %5 [ %6 ] %7 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 47,
			  "output" : "Model",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "m1",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ExecType/streaming'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ExecType/streaming",
			  "message0" : "streaming",
			  
			  "colour" : 289,
			  "output" : "ExecType",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "streaming",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Duplicator/dupl'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Duplicator/dupl",
			  "message0" : "duplicate %1 %2 ( %3 %4 ) %5 -> %6 [ %7 ] %8 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Port",
				  "type" : "input_statement",
				  "check" : ["Port"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 281,
			  "output" : "Duplicator",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "dupl",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['LogicalOp/an'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "LogicalOp/an",
			  "message0" : "AND",
			  
			  "colour" : 183,
			  
			  "previousStatement" : "LogicalOp",
			  "nextStatement" : "LogicalOp",
			  "inputsInline" : true,
			  "tooltip" : "an",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/gt'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/gt",
			  "message0" : "%1 > %2 %3 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 187,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "gt",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Typ/float'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Typ/float",
			  "message0" : "float",
			  
			  "colour" : 358,
			  
			  "previousStatement" : "Typ",
			  "nextStatement" : "Typ",
			  "inputsInline" : true,
			  "tooltip" : "float",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/joule'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/joule",
			  "message0" : "J",
			  
			  "colour" : 311,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "joule",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ModelConfiguration/mc2'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ModelConfiguration/mc2",
			  "message0" : "config %1 ( %2 ) %3 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 93,
			  "output" : "ModelConfiguration",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "mc2",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Dataprocess/dataprocess'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Dataprocess/dataprocess",
			  "message0" : "dataprocess %1 %2 ( %3 ) %4 -> %5 [ %6 ] %7 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 128,
			  "output" : "Dataprocess",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "dataprocess",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/kelvin'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/kelvin",
			  "message0" : "K",
			  
			  "colour" : 16,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "kelvin",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Sensor/sens'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Sensor/sens",
			  "message0" : "sensor %1 %2 -> %3 [ %4 ] %5 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 272,
			  "output" : "Sensor",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "sens",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/assign'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/assign",
			  "message0" : "%1 = %2 %3 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 125,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "assign",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/meter'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/meter",
			  "message0" : "m",
			  
			  "colour" : 37,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "meter",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['CommunicationManager/cm'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "CommunicationManager/cm",
			  "message0" : "Communication_manager:",
			  
			  "colour" : 152,
			  "output" : "CommunicationManager",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "cm",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/min'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/min",
			  "message0" : "%1 - %2 %3 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 90,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "min",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ComponentManager/cm'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ComponentManager/cm",
			  "message0" : "Component_manager:",
			  
			  "colour" : 20,
			  "output" : "ComponentManager",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "cm",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Unit/basic_unit'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Unit/basic_unit",
			  "message0" : "",
			  
			  "colour" : 255,
			  
			  "previousStatement" : "Unit",
			  "nextStatement" : "Unit",
			  "inputsInline" : true,
			  "tooltip" : "basic_unit",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Component/ux'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Component/ux",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "UX",
				  "type" : "input_value",
				  "check" : ["UX"]
				},
				
			],
			  "colour" : 108,
			  
			  "previousStatement" : "Component",
			  "nextStatement" : "Component",
			  "inputsInline" : true,
			  "tooltip" : "ux",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['EspecialExp/cond'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "EspecialExp/cond",
			  "message0" : "if %1 %2 : %3 %4 else %5 : %6 %7 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 37,
			  
			  "previousStatement" : "EspecialExp",
			  "nextStatement" : "EspecialExp",
			  "inputsInline" : true,
			  "tooltip" : "cond",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Component/bd'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Component/bd",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "DB",
				  "type" : "input_value",
				  "check" : ["DB"]
				},
				
			],
			  "colour" : 228,
			  
			  "previousStatement" : "Component",
			  "nextStatement" : "Component",
			  "inputsInline" : true,
			  "tooltip" : "bd",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['TimeUnit/sec'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "TimeUnit/sec",
			  "message0" : "s",
			  
			  "colour" : 13,
			  "output" : "TimeUnit",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "sec",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/funcCall'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/funcCall",
			  "message0" : "%1 ( %2 %3 ) %4 ",
			  "args0" : [
				{
				  "name" : "lex",
				  "type" : "field_input",
				  "text" : "Expression"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "ExpressionList",
				  "type" : "input_value",
				  "check" : ["ExpressionList"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 233,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "funcCall",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/second'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/second",
			  "message0" : "s",
			  
			  "colour" : 75,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "second",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Connector/cn'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Connector/cn",
			  "message0" : "connect %1 %2 ( %3 %4 %5 . %6 %7 , %8 %9 %10 . %11 %12 ) %13 -> %14 %15 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "stmt",
				  "type" : "input_statement",
				  "check" : ["", "epsilon"]
				},
				  	{
				  "name" : "src_comp",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "out_port",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "stmt",
				  "type" : "input_statement",
				  "check" : ["", "epsilon"]
				},
				  	{
				  "name" : "dst_comp",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "in_port",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "ExchMethod",
				  "type" : "input_value",
				  "check" : ["ExchMethod"]
				},
				
			],
			  "colour" : 337,
			  "output" : "Connector",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "cn",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['CommComp/aggregator'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "CommComp/aggregator",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "Aggregator",
				  "type" : "input_value",
				  "check" : ["Aggregator"]
				},
				
			],
			  "colour" : 264,
			  
			  "previousStatement" : "CommComp",
			  "nextStatement" : "CommComp",
			  "inputsInline" : true,
			  "tooltip" : "aggregator",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['SrcExe/sr2'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "SrcExe/sr2",
			  "message0" : "source %1 %2 ( %3 ) %4 -> %5 %6 : %7 %8 def: %9 %10 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "ExecType",
				  "type" : "input_value",
				  "check" : ["ExecType"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Trigger",
				  "type" : "input_value",
				  "check" : ["Trigger"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "TempDef",
				  "type" : "input_value",
				  "check" : ["TempDef"]
				},
				
			],
			  "colour" : 159,
			  "output" : "SrcExe",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "sr2",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ExecType/time'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ExecType/time",
			  "message0" : "time_specific",
			  
			  "colour" : 254,
			  "output" : "ExecType",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "time",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/ampere'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/ampere",
			  "message0" : "A",
			  
			  "colour" : 143,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "ampere",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['CoSimExe/c3'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "CoSimExe/c3",
			  "message0" : "cosim %1 %2 ( %3 ) %4 -> %5 continuous %6 : %7 %8 def: %9 %10 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Trigger",
				  "type" : "input_value",
				  "check" : ["Trigger"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "TempDef",
				  "type" : "input_value",
				  "check" : ["TempDef"]
				},
				
			],
			  "colour" : 286,
			  "output" : "CoSimExe",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "c3",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/div'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/div",
			  "message0" : "%1 / %2 %3 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 104,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "div",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['EspecialExp/loop'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "EspecialExp/loop",
			  "message0" : "while %1 %2 : %3 %4 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 356,
			  
			  "previousStatement" : "EspecialExp",
			  "nextStatement" : "EspecialExp",
			  "inputsInline" : true,
			  "tooltip" : "loop",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ExecComp/sinkexe'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ExecComp/sinkexe",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "SinkExe",
				  "type" : "input_value",
				  "check" : ["SinkExe"]
				},
				
			],
			  "colour" : 226,
			  
			  "previousStatement" : "ExecComp",
			  "nextStatement" : "ExecComp",
			  "inputsInline" : true,
			  "tooltip" : "sinkexe",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['DB/onlyins'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "DB/onlyins",
			  "message0" : "db %1 %2 ( %3 ) %4 -> %5 None %6 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 116,
			  "output" : "DB",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "onlyins",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/newton'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/newton",
			  "message0" : "N",
			  
			  "colour" : 107,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "newton",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Trigger_type'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Trigger_type",
			  "message0" : "stop",
			  
			  "colour" : 26,
			  "output" : "Trigger_type",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['PortList/portList'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "PortList/portList",
			  "message0" : "",
			  
			  "colour" : 40,
			  
			  "previousStatement" : "PortList",
			  "nextStatement" : "PortList",
			  "inputsInline" : true,
			  "tooltip" : "portList",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['UX/bothports'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "UX/bothports",
			  "message0" : "ux %1 %2 ( %3 ) %4 -> %5 [ %6 ] %7 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 84,
			  "output" : "UX",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "bothports",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Service/commmng'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Service/commmng",
			  "message0" : "Service Name %1 : %2 %3 %4 %5 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "ComponentManager",
				  "type" : "input_value",
				  "check" : ["ComponentManager"]
				},
				  	{
				  "name" : "CommunicationManager",
				  "type" : "input_value",
				  "check" : ["CommunicationManager"]
				},
				
			],
			  "colour" : 120,
			  
			  
			  
			  "inputsInline" : false,
			  "tooltip" : "",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['TimeUnit/milisec'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "TimeUnit/milisec",
			  "message0" : "ms",
			  
			  "colour" : 78,
			  "output" : "TimeUnit",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "milisec",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ExchMethod/lifo'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ExchMethod/lifo",
			  "message0" : "LIFO",
			  
			  "colour" : 129,
			  "output" : "ExchMethod",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "lifo",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/kilogram'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/kilogram",
			  "message0" : "kg",
			  
			  "colour" : 97,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "kilogram",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Decimal'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Decimal",
			  "message0" : "%1 . %2 %3 ",
			  "args0" : [
				{
				  "name" : "DecimalName",
				  "type" : "field_number",
				  "value" : 0
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "DecimalName",
				  "type" : "field_number",
				  "value" : 0
				},
				
			],
			  "colour" : 320,
			  "output" : "Decimal",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Unit/power_pos_num'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Unit/power_pos_num",
			  "message0" : "%1 ^ %2 %3 ",
			  "args0" : [
				{
				  "name" : "BasicUnit",
				  "type" : "input_statement",
				  "check" : ["BasicUnit"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "lex",
				  "type" : "input_value",
				  "check" : ["Natural"]
				},
				
			],
			  "colour" : 182,
			  
			  "previousStatement" : "Unit",
			  "nextStatement" : "Unit",
			  "inputsInline" : true,
			  "tooltip" : "power_pos_num",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['CommComp/splitter'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "CommComp/splitter",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "Splitter",
				  "type" : "input_value",
				  "check" : ["Splitter"]
				},
				
			],
			  "colour" : 25,
			  
			  "previousStatement" : "CommComp",
			  "nextStatement" : "CommComp",
			  "inputsInline" : true,
			  "tooltip" : "splitter",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['SinkExe/sn2'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "SinkExe/sn2",
			  "message0" : "sink %1 %2 ( %3 ) %4 -> %5 %6 : %7 %8 def: %9 %10 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "ExecType",
				  "type" : "input_value",
				  "check" : ["ExecType"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Trigger",
				  "type" : "input_value",
				  "check" : ["Trigger"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "TempDef",
				  "type" : "input_value",
				  "check" : ["TempDef"]
				},
				
			],
			  "colour" : 262,
			  "output" : "SinkExe",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "sn2",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['TempDef/frequency'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "TempDef/frequency",
			  "message0" : "freq %1 = %2 %3 ( %4 %5 ) %6 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "lex",
				  "type" : "input_value",
				  "check" : ["Natural"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "TimeUnit",
				  "type" : "input_value",
				  "check" : ["TimeUnit"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 247,
			  "output" : "TempDef",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "frequency",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ExecType/invoke'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ExecType/invoke",
			  "message0" : "invoke",
			  
			  "colour" : 142,
			  "output" : "ExecType",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "invoke",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ExecutionManager/em'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ExecutionManager/em",
			  "message0" : "Execution_manager:",
			  
			  "colour" : 7,
			  "output" : "ExecutionManager",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "em",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['CoSimExe/c1'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "CoSimExe/c1",
			  "message0" : "cosim %1 %2 ( %3 ) %4 -> %5 invoke %6 : %7 %8 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Trigger",
				  "type" : "input_value",
				  "check" : ["Trigger"]
				},
				
			],
			  "colour" : 139,
			  "output" : "CoSimExe",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "c1",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['SimTime/sm'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "SimTime/sm",
			  "message0" : "RT",
			  
			  "colour" : 307,
			  "output" : "SimTime",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "sm",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['CommComp/connector'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "CommComp/connector",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "Connector",
				  "type" : "input_value",
				  "check" : ["Connector"]
				},
				
			],
			  "colour" : 165,
			  
			  "previousStatement" : "CommComp",
			  "nextStatement" : "CommComp",
			  "inputsInline" : true,
			  "tooltip" : "connector",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ExecComp/cosimexe'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ExecComp/cosimexe",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "CoSimExe",
				  "type" : "input_value",
				  "check" : ["CoSimExe"]
				},
				
			],
			  "colour" : 70,
			  
			  "previousStatement" : "ExecComp",
			  "nextStatement" : "ExecComp",
			  "inputsInline" : true,
			  "tooltip" : "cosimexe",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ExchMethod/pq'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ExchMethod/pq",
			  "message0" : "PQ",
			  
			  "colour" : 355,
			  "output" : "ExchMethod",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "pq",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['BasicUnit/grams'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "BasicUnit/grams",
			  "message0" : "g",
			  
			  "colour" : 47,
			  
			  "previousStatement" : "BasicUnit",
			  "nextStatement" : "BasicUnit",
			  "inputsInline" : true,
			  "tooltip" : "grams",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Triggerdef/i'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Triggerdef/i",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "lex",
				  "type" : "field_input",
				  "text" : "Triggerdef"
				},
				
			],
			  "colour" : 313,
			  
			  "previousStatement" : "Triggerdef",
			  "nextStatement" : "Triggerdef",
			  "inputsInline" : true,
			  "tooltip" : "i",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Component/model'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Component/model",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "Model",
				  "type" : "input_value",
				  "check" : ["Model"]
				},
				
			],
			  "colour" : 26,
			  
			  "previousStatement" : "Component",
			  "nextStatement" : "Component",
			  "inputsInline" : true,
			  "tooltip" : "model",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/dot'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/dot",
			  "message0" : "%1 . %2 %3 ( %4 %5 ) %6 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "id",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "opt",
				  "type" : "input_statement",
				  "check" : ["Expression", "epsilon"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 95,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "dot",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['SrcExe/sr'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "SrcExe/sr",
			  "message0" : "source %1 %2 ( %3 ) %4 -> %5 %6 : %7 %8 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "ExecType",
				  "type" : "input_value",
				  "check" : ["ExecType"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Trigger",
				  "type" : "input_value",
				  "check" : ["Trigger"]
				},
				
			],
			  "colour" : 94,
			  "output" : "SrcExe",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "sr",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Typ/boolean'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Typ/boolean",
			  "message0" : "bool",
			  
			  "colour" : 321,
			  
			  "previousStatement" : "Typ",
			  "nextStatement" : "Typ",
			  "inputsInline" : true,
			  "tooltip" : "boolean",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Transformation/trs'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Transformation/trs",
			  "message0" : "transform %1 %2 ( %3 ) %4 -> %5 [ %6 ]: %7 def: %8 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 154,
			  "output" : "Transformation",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "trs",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['UX/onlyouts'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "UX/onlyouts",
			  "message0" : "ux %1 %2 -> %3 [ %4 ] %5 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 28,
			  "output" : "UX",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "onlyouts",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/comp'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/comp",
			  "message0" : "%1 == %2 %3 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				
			],
			  "colour" : 194,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "comp",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/ids'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/ids",
			  "message0" : "%1 : %2 %3 ",
			  "args0" : [
				{
				  "name" : "lid",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "rid",
				  "type" : "field_input",
				  "text" : ""
				},
				
			],
			  "colour" : 239,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "ids",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Actuator/actuator'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Actuator/actuator",
			  "message0" : "actuator %1 %2 ( %3 ) %4 -> %5 None %6 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "name",
				  "type" : "field_input",
				  "text" : ""
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 65,
			  "output" : "Actuator",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "actuator",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Expression/component'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Expression/component",
			  "message0" : "%1 . %2 %3 ",
			  "args0" : [
				{
				  "name" : "Expression",
				  "type" : "input_statement",
				  "check" : ["Expression"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "id",
				  "type" : "field_input",
				  "text" : ""
				},
				
			],
			  "colour" : 282,
			  
			  "previousStatement" : "Expression",
			  "nextStatement" : "Expression",
			  "inputsInline" : true,
			  "tooltip" : "component",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['CommComp/transformation'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "CommComp/transformation",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "Transformation",
				  "type" : "input_value",
				  "check" : ["Transformation"]
				},
				
			],
			  "colour" : 149,
			  
			  "previousStatement" : "CommComp",
			  "nextStatement" : "CommComp",
			  "inputsInline" : true,
			  "tooltip" : "transformation",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Eval/e'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Eval/e",
			  "message0" : "[ %1 ] %2 = %3 eval %4 ( %5 components %6 = %7 [ %8 ] %9 , %10 vars_assigment %11 = %12 [ %13 ] %14 ) %15 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 331,
			  
			  "previousStatement" : "Eval",
			  "nextStatement" : "Eval",
			  "inputsInline" : true,
			  "tooltip" : "e",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['ExecComp/srcexe'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "ExecComp/srcexe",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "SrcExe",
				  "type" : "input_value",
				  "check" : ["SrcExe"]
				},
				
			],
			  "colour" : 1,
			  
			  "previousStatement" : "ExecComp",
			  "nextStatement" : "ExecComp",
			  "inputsInline" : true,
			  "tooltip" : "srcexe",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Trigger/event'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Trigger/event",
			  "message0" : "trigger %1 -> %2 event %3 . %4 %5 : %6 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "Trigger_type",
				  "type" : "input_value",
				  "check" : ["Trigger_type"]
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 128,
			  "output" : "Trigger",
			  
			  
			  "inputsInline" : true,
			  "tooltip" : "event",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Unit/complex'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Unit/complex",
			  "message0" : "[ %1 ] %2 ",
			  "args0" : [
				{
				  "name" : "",
				  "type" : "input_dummy"
				},
				  	{
				  "name" : "",
				  "type" : "input_dummy"
				},
				
			],
			  "colour" : 303,
			  
			  "previousStatement" : "Unit",
			  "nextStatement" : "Unit",
			  "inputsInline" : true,
			  "tooltip" : "complex",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.Blocks['Triggerdef/t'] = {
	init: function() {
		this.jsonInit(
			{
			  "type" : "Triggerdef/t",
			  "message0" : "%1 ",
			  "args0" : [
				{
				  "name" : "TempDef",
				  "type" : "input_value",
				  "check" : ["TempDef"]
				},
				
			],
			  "colour" : 275,
			  
			  "previousStatement" : "Triggerdef",
			  "nextStatement" : "Triggerdef",
			  "inputsInline" : true,
			  "tooltip" : "t",
			  "helpUrl" : ""
			}
		);
	}
}
Blockly.BlockSvg.START_HAT = true;
var workspace = Blockly.inject('blockDiv', {
	toolbox: document.getElementById('toolbox'),
	collapse: true,
   toolboxPosition: 'start', // end
   trashcan: true
});
	

 //Storage options
BlocklyStorage.backupOnUnload();	
window.setTimeout(BlocklyStorage.restoreBlocks, 0);
function xmlText() {
	var xml = Blockly.Xml.workspaceToDom(workspace);
	var xml_text = Blockly.Xml.domToPrettyText(xml);
	document.getElementById('textarea').value = xml_text;
}
	