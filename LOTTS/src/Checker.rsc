module Checker 

import IO;
import Type;
import LOTTS2;
import ParseTree;
import List;
import Set;
import String;
public list[Id] comp_names = [];

public map[str name, map[str portype , map [str concept , map[str,str] val] ports] concepts] compStructure =("glob":("inputs":(), "outputs":()));
public map[str, str] compType = ("glob":"global");

public map[str, list[str]] areaComp = ("source": ["sensor","db","dataprocess","ux"],"sink":["actuator","db","dataprocess","ux"],
                                        "cosim":["model"],"general":["global"], "comm":["connector","transformator","duplicator", "spliter","switch","aggregator"]);


Tree parseProgram(loc l) =  parse(#start[Service],l,allowAmbiguity = true);



bool loadAndCheck(loc c) 
    {
        Tree tree =  parseProgram(c);
        
        // return true;
        
        return checkWellformedness(tree.top);

    }

bool checkWellformedness ((Service) s)
    {
        println("The name of the service is <s.name>");
        comp_count = 0;
        comp_names = [];
        compType = ("glob":"global");
        CompMng_check = checkWellformedness(s.cm);
        CommMng_ckeck = true;
        ExecMng_check = true;
        // println(typeOf(d));
        if (s has cmm){CommMng_ckeck = checkWellformedness(s.cmm);}
        else{CommMng_ckeck = true;}
        
        if (s has em){CommMng_ckeck = checkWellformedness(s.em);}
        else{ExecMng_check = true;}


        correct = CompMng_check && CommMng_ckeck && ExecMng_check;
     return correct;

    }

    
bool checkWellformedness ((ComponentManager) `Component_manager: <Component+ components>`)
{   
    
    s_count =0; a_count = 0; u_count =0;b_count=0; m_count =0; dp_count = 0; g_count = 0;
    comp_mng = true;
    for (comp<-components){
        
        switch(comp){
            case(Component) `<Sensor s>`: {s_count+=1; extractComp(s, "sensor");}
            case(Component) `<Actuator a>`: {a_count+=1; extractComp(a, "actuator");}
            case(Component) `<UX u>`: {u_count+=1;extractComp(u, "ux");}
            case(Component) `<DB b>`: {b_count+=1;extractComp(b, "db");}
            case(Component) `<Model m>`:{m_count+=1; extractComp(m, "model");}
            case(Component) `<Dataprocess dp>`: {dp_count+=1;extractComp(dp, "dataprocess");}
            case(Component) `<Global g>`: {g_count+=1; checkWellformedness(g, g_count); }
        }
    }
        println("The systems is composed of:");
        if(s_count != 0 ) {println("    <s_count> sensors ");}
        if(a_count != 0 ) {println("    <a_count> actuators");}
        if(u_count != 0 ) {println("    <u_count> user interfaces");}
        if(b_count != 0 ) {println("    <b_count> databases");}
        if(m_count != 0 ) {println("    <m_count> models"); }
        if(dp_count != 0 ) {println("   <dp_count> dataprocessing units");}
        // if(g_count != 0 ) {println("<g_count> global variables");}
        // println(<comp_names>);
        // println(size(comp_types["sensor"]));
    return comp_mng;
}



bool checkWellformedness((Global) g , int count)
    {
        correct = true;
        switch(g)
            {
            case(Global) `global  ( <{Port ","}* ins> ) -\> None`: {
                // componentslist["glob"] = componentslist["glob"] + ("inputs":ins, "outputs":[]);
                extractComp(g, "global");
                }
            case(Global) `global  ( <{Port ","}* ins> ) -\> None: <EspecialExp+ exp>`: 
                { 
                // componentslist["glob"] = componentslist["glob"] + ("inputs":ins, "outputs":[]);
                extractComp(g, "global");
                for (e<-exp){
                
                      if(e is assign){correct =  true;}
                       else{println("Error:Global variables are defined as assigments with units"); correct = false; return correct;}
                       }
                       }
                
            case(Global) `global  -\> None: <EspecialExp+ exp>`: 
                {
                // componentslist["glob"] = componentslist["glob"] + ("inputs":[], "outputs":[]);
                for (e<-exp){
                
                      if(e is assign){correct =  true;}
                       else{println("Error:Global variables are defined as assigments with units"); correct = false;}
                       }
                }
                
            }
            if (count > 1){correct = false; println("there should only be one global component, please merge");}
            return correct;
    }


bool checkWellformedness ((CommunicationManager) `Communication_manager: <CommComp+ cmm>`)
{
    // check of connectors
    conn_count= 0 ; dup_count = 0; split_count = 0; swit_count = 0; agg_count = 0;trans_count =0 ;
    for (comp <- cmm)
        {
            // println("working on it");
            switch(comp){
                case(CommComp) `<Connector connect>`: {conn_count+=1 ;
                    correct = checkWellformedness(connect); 
                    println("is the connector <connect.name> correct? = <correct>");}
                case(CommComp) `<Duplicator d>`:{dup_count+=1;extractComp(d, "duplicator");
                    correct = checkCommConsistency (d, "duplicator");
                    println("is the duplicator correct? = <correct>\n");}
                case(CommComp) `<Splitter sp>`:{split_count+=1;extractComp(sp, "splitter");
                    correct = checkCommConsistency (sp, "splitter");
                    println("is the splitter correct? = <correct>\n");}
                case(CommComp) `<Aggregator agg>`:{agg_count+=1;extractComp(agg, "aggregator");
                    correct = checkCommConsistency (agg, "aggregator");
                    println("is the aggregator correct? = <correct>\n");}
                case(CommComp) `<Switch sw>`:{swit_count+=1;extractComp(sw, "switch");
                    consistent = checkCommConsistency (sw, "switch"); 
                    correct = checkWellformedness(sw);
                    println("is the switch correct? = <correct && consistent>\n");}
                case(CommComp) `<Transformation tra>`:{trans_count+=1;extractComp(tra, "transformator");}

                default: println("");
            }
        }
    println("\nComponents of connections are:");
    if(conn_count != 0 ) {println("    <conn_count> connections ");}
    if(dup_count != 0 ) {println("    <dup_count> duplicators ");}
    if(split_count != 0 ) {println("    <split_count> spliters ");}
    if(agg_count != 0 ) {println("    <agg_count> aggregators ");}
    if(swit_count != 0 ) {println("    <swit_count> switches ");}
    if(trans_count != 0 ) {println("    <trans_count> transformers ");}
    // check of units 
    return true;
}

bool checkWellformedness((Connector) conn)
{
    areComponentsPresent = true;
    correctPorts = true;
    correctConsistency = true;

    // 1. check that names are unique, also compare with other components
    name = "<conn.name>";
    connUniqueName = nameChecker (name);   
    add_name(conn.name , "connector") ;
    if (connUniqueName == true){
        // add_name(conn.name , "connector");
        println("");        
    }
    else{
        println("The connector name <name> is unique, change it");
         return false;
        }
    //2. check that all Id of components exists and that Id of input and/or outputs 
    // also exists respect to the component
    src = "<conn.src_comp>"; dst= "<conn.dst_comp>";
    outport = "<conn.out_port>"; inport = "<conn.in_port>";
    srcdefine = src in compStructure<0>;
    dstdefine = dst in compStructure<0>;

    areComponentsPresent = srcdefine && dstdefine;
    if (areComponentsPresent == false)
        {
            println("One or non of the components in the connector <conn.name> does not exist, please correct them"); 
            if ((src in compStructure<0>)== false){println("Component <src> does not exists");}
            if ((dst in compStructure<0>)== false){println("Component <dst> does not exists");}

            //return false;
        }


    //3. check that flow definition is always output -> input
   if (areComponentsPresent == true){
        isOutput = outport in compStructure[src]["outputs"]<0>;
        if (isOutput == false){
            println("<outport> is not an output of component <src>");
            // return false;
        }

        // println(outport in compStructure[src]["outputs"]<0>);

        // println("these are the inputs of the <dst> looking for for input <inport>");
        isInput = inport in compStructure[dst]["inputs"]<0>;
        if (isInput == false){
            println("<inport> is not an output of component <dst>");
            // return false;
        }
        // println(inport in compStructure[dst]["inputs"]<0>);

        correctPorts = isOutput && isInput;
   }
//     //4. check units, equal for inputs and outputs
    if (correctPorts == true){
        correctConsistency = unitChecker(src, outport, dst, inport);
    }

    correctForm = areComponentsPresent && correctPorts && correctConsistency;
    
    if (correctForm== true){
        println("Connector: <name> is correctly created");
    } else{println("Connector: <name> is not correctly created");}

    return correctForm;
}

bool checkWellformedness((Switch) sw){
    hasAssigs = true;
    isCond = sw.exp is cond;
    if (isCond == true) {
        hasAssigs = (sw.exp.s is assign) && (sw.exp.ss is assign);
        if (hasAssigs == false){println("switch <sw.name>  needs to be define using assig expressions, please correct");}
    } else {
        println("switch <sw.name> needs to be define using conditionals and assigment expressions, please correct");
    }
    
    // println(sw.exp is cond);
    // println(sw.exp.e);
    // println(sw.exp.s is assign);
    // println(sw.exp.s.l.id);
    // println(sw.exp.s.r.id);
    // println(sw.exp.ss is assign);
    // println(sw.exp.ss.l.id);
    // println(sw.exp.ss.r.id);
    correct = isCond && hasAssigs;
    // println(correct);
    return correct;
    // return true;
}

bool checkCommConsistency (comp, str class)
{
    name = "<comp.name>";
    
    correctUnit = true;
    inputName = "";
    outputName ="";
    checkConsist = [];
    
    switch(class){
        case "duplicator": {
            inputName = "<comp.ins.name>";
            count = 0;
            for (outs<-comp.outs){
                tempOut = "<outs.name>";
                checkConsist = checkConsist + unitChecker(name, tempOut, name, inputName);
                // println("dup unit and format checker input <inputName> and <tempOut> is <correctUnit>");
                
                if (checkConsist[count] == false){
                    println("<class> <name>: input <inputName> is not consistent with output <tempOut>");
                }
                correctUnit = correctUnit && checkConsist[count];
                count+=1;
            }
            if (correctUnit == true){println("<class> <name> has unit and data format consistency");}
        }
        case "switch":{
            outputName = "<comp.outs.name>"; 
            count = 0;   
            for (ins<-comp.ins){                
                tempIn = "<ins.name>";
                correctUnit = unitChecker(name, outputName, name, tempIn);
                if (correctUnit== false){
                    println("Inputs in component <name> must have the same units and data types, correct it");
                }
            }
        }

        case "splitter":{
            inputName = "<comp.ins.name>";
            cmpxUnit = compStructure[name]["inputs"][inputName]["unit"];
            cmpxFormat = compStructure[name]["inputs"][inputName]["type"];
            // println(unit1);
            // println(dataformat1);
            inputsUnit = unpackCmpxData(cmpxUnit);
            inputsFormat = unpackCmpxData(cmpxFormat);
            // println(inputsFormat);
            count = 0;
            //compare if size of inputs & outputs are equal
            inputsSize = size(inputsUnit);
            outputsSize = size(compStructure[name]["outputs"]<0>);
            sizecomparison = (inputsSize == outputsSize);

            if( sizecomparison == false){
                println("Error: splitter <name> does not have equal number of complex inputs elements and output ports");}
            else{
                for (outs<-comp.outs){
                    tempOut = "<outs.name>";
                    OutUnit = compStructure[name]["outputs"][tempOut]["unit"];
                    OutType = compStructure[name]["outputs"][tempOut]["type"];
                    CheckUnit = inputsUnit[count] == OutUnit;
                    CheckType = inputsFormat[count] == OutType;
                    checkConsist =  checkConsist + (CheckType && CheckUnit);
                    // checkConsist = checkConsist + unitChecker(name, tempOut, name, inputsName[count]);
                    // println("dup unit and format checker input <inputName> and <tempOut> is <correctUnit>");
                    
                    if (checkConsist[count] == false){
                        println("<class> <name>: input <inputName> is not consistent with output <tempOut>");
                    }
                    correctUnit = correctUnit && checkConsist[count];
                    count+=1;
                    
                    }
            }
            
            }

        case "aggregator":{
            outname = "<comp.outs.name>";
            cmpxUnit = compStructure[name]["outputs"][outname]["unit"];
            cmpxFormat = compStructure[name]["outputs"][outname]["type"];
            outputsUnit = unpackCmpxData(cmpxUnit);
            outputsFormat = unpackCmpxData(cmpxFormat);
            
            count = 0;
            //compare if size of inputs & outputs are equal
            outputsSize = size(outputsUnit);
            inputsSize = size(compStructure[name]["inputs"]<0>);
            sizecomparison = (inputsSize == outputsSize);
            
            if( sizecomparison == false){
                println("Error: splitter <name> does not have equal number of complex inputs elements and output ports");}
            else{
                for (ins<-comp.ins){
                    tempIns = "<ins.name>";
                    InUnit = compStructure[name]["inputs"][tempIns]["unit"];
                    InType = compStructure[name]["inputs"][tempIns]["type"];
                    CheckUnit = outputsUnit[count] == InUnit;
                    CheckType = outputsFormat[count] == InType;
                    checkConsist =  checkConsist + (CheckType && CheckUnit);
                    // checkConsist = checkConsist + unitChecker(name, tempOut, name, inputsName[count]);
                    // println("dup unit and format checker input <inputName> and <tempOut> is <correctUnit>");
                    
                    if (checkConsist[count] == false){
                        println("<class> <name>: input <inputName> is not consistent with output <tempOut>");
                    }
                    correctUnit = correctUnit && checkConsist[count];
                    count+=1;
                    
                    }
            }
            
            }
    
    }
    

    return correctUnit;
    


}

bool checkWellformedness ((ExecutionManager) `Execution_manager: <ExecComp+ execcomp>`)
{
    wellformed = true;
    for (comp <- execcomp){
        // nameU = comp_nameChecker(comp.name);
        // println(<comp>);
        switch(comp){
            case(ExecComp) `<SrcExe srcexe>`:{
                nameU = comp_nameChecker(srcexe.name);
                // println(nameU);
                correctForm = checkWellformedness(srcexe);
                correctDefined = areaCompCheck(srcexe.srcComp,"source");
                println("area <srcexe.name> is correctly defined? = <correctDefined>");
                wellformed = wellformed && nameU && correctForm && correctDefined;
                }
            case(ExecComp) `<SinkExe sinkexe>`:{
                nameU = comp_nameChecker(sinkexe.name);
                // println(nameU);
                correctDefined = areaCompCheck(sinkexe.sinkComp,"sink");
                println("area <sinkexe.name> is correctly defined? = <correctDefined>");
                wellformed = wellformed && nameU && correctDefined;
                }
            case(ExecComp) `<CoSimExe cosimexe>`:{
                nameU = comp_nameChecker(cosimexe.name);
                // println(nameU);
                correctDefined = areaCompCheck(cosimexe.cosimComp,"cosim");
                println("area <cosimexe.name> is correctly defined? = <correctDefined>");
                wellformed = wellformed && nameU && correctDefined;
                }
        }
    }
    return wellformed;
}

bool checkWellformedness((SrcExe) srcexe){
    correct =  true;
    if (srcexe.tr is signal){
        correct = false;
        println("The source area component <srcexe.name> can not have trigger of time signal, please correct");

        }

    return correct;
}

bool areaCompCheck(components, str areaType){
    areaCompDef = true;
    areaComps =[];
    if (areaType in areaComp<0>){
        for (comp <- components){
            compName = "<comp>";
            if (compName in compType) 
                {elementType = compType[compName];
                if (elementType in areaComp[areaType] == false){
                    println("Component <compName> is of type <elementType> is not the right type for area type <areaType>");}
                areaCompDef = areaCompDef && (elementType in areaComp[areaType]);

                // println("comp <compName> is in <areaType>? = <areaCompDef>");
                }
            else {println("Component <compName> not yet defined ");
                areaCompDef = false;}
            // println("comp <compName> exists? = <exitsComp> ");
            
            // println(elementType);
            
        }

        
        ;}
    // println("area designed correctly ? = <areaCompDef>");
    return areaCompDef;
}

// functions that help the checking

bool comp_nameChecker (Id comp_name)
{
    cn = "<comp_name>";
    correctness = !(cn in compType<0>);    
    return correctness;
}

bool nameChecker (str comp_name)
{
    cn = comp_name;
    correctness = !(cn in compType<0>);    
    return correctness;
}

void add_name(Id name , str class)
{
    comp_names = comp_names + name;
    // comp_types[class] = comp_types[class] + name;
    compType["<name>"] = class;
    // compType = class;

    
}

bool unitChecker(str src, str outport, str dst, str inport)
{   
    checkType = true; checkUnits = true;

    src_unit= compStructure[src]["outputs"][outport]["unit"];
    src_datatype = compStructure[src]["outputs"][outport]["type"];
    // println("source unit is <src_unit> and type is <src_datatype>");

    dst_unit= compStructure[dst]["inputs"][inport]["unit"];
    dst_datatype = compStructure[dst]["inputs"][inport]["type"];
    // println("destination unit is <dst_unit> and type is <dst_datatype>");
    //check wether datatype is equal of input and outputs
    if (src_datatype == dst_datatype){
        checkType == true;
        }else{
            checkType = false; 
            println("datatype is not equal between <src> output(type:<src_datatype>) and <dst> input(type:<dst_datatype>)");   
        }
    //check wether units is equal of input and outputs
    if (src_unit == dst_unit){
        checkUnits == true;
        }else{
            checkUnits = false; 
            println("units are not equal between <src> output(unit:<src_unit>) and <dst> input(unit:<dst_unit>)");   
        }
    
    return (checkType && checkUnits);
}

list[str] unpackCmpxData(str complexData){
    strLength = size(complexData)-1;
    identifyComp = findAll(complexData,",")+ strLength ;
    nComp = size(identifyComp) ;
    cList = [];
    
    indx = 1;
    
    for (c <- [0..nComp]){
        
        cList = cList +substring(complexData,indx,identifyComp[c]);
        // println(cList[c]);
        indx = identifyComp[c]+1;
        // println(indx);
    }
    return cList;
}

void extractComp(comp, str class)
{
    name = "non";
    // inputs = "non";
    portCase = "non";
    portin = ("inputs":());
    portout = ("outputs":());
    correctform = true;
    if (class == "global"){name = "glob";}
    else {
        name = "<comp.name>";
        // println(name);
        correctform = comp_nameChecker(comp.name);
        if (correctform == true) 
        { 
        println("Component name <name> is unique");
        add_name(comp.name , class);
        compStructure = compStructure + (name:("inputs":(), "outputs":()));
        }
        else {println("Components\' names have to be unique <name> is not unique");}
        
        }
    if (correctform == true)
    
    
        {
            if (class == "sensor" || (class == "ux" && comp is onlyouts) || (class == "db" && comp is onlyouts)) 
                { 
                portCase="outs";//inputs = []; outputs = comp.outs; 
                }
            if (class == "actuator" || (class == "ux" && comp is onlyins) || (class == "db" && comp is onlyins) ) 
                {
                portCase="ins";//inputs = comp.ins; outputs = [];
                }
            if ((class == "ux" && comp is bothports) || (class == "db" && comp is bothports) || class == "model" || class == "dataprocess"
                || class == "duplicator"|| class == "switch"|| class == "aggregator"|| class == "splitter"|| class == "transformator")
                {
                portCase="both";//inputs = comp.ins; outputs = comp.outs; 
                // println("<typeOf(comp.outs)>");
                }
            // println("<name> : <portCase>")          ;
            if (portCase == "ins" || portCase == "both")
                if (class == "duplicator" || class == "splitter" ){
                    j= comp.ins;
                    input = ("<j.name>":("type":"<j.typ>","unit":"<j.units>"));
                    portin["inputs"] =  portin["inputs"] + input;
                    compStructure[name] = compStructure[name]+portin;
                }else{
                    {for (j<-comp.ins)
                        {
                        input = ("<j.name>":("type":"<j.typ>","unit":"<j.units>"));
                        portin["inputs"] =  portin["inputs"] + input;
                        // comps["glob"]["inputs"] = comps["glob"]["inputs"] + input;
                        }
                        // println(compStructure);
                        compStructure[name] = compStructure[name]+portin;
                    }
                }
                
            if (portCase == "outs" || portCase == "both")
                if (class == "aggregator" || class == "switch" ){
                    j= comp.outs;
                    output = ("<j.name>":("type":"<j.typ>","unit":"<j.units>"));
                    portout["outputs"] =  portout["outputs"] + output;
                    compStructure[name] = compStructure[name]+portout;
                }else{
                    {for (j<-comp.outs)
                        {
                        output = ("<j.name>":("type":"<j.typ>","unit":"<j.units>"));
                        portout["outputs"] =  portout["outputs"] + output;
                        // comps["glob"]["inputs"] = comps["glob"]["inputs"] + input;
                        }
                        // println(compStructure);
                        compStructure[name] = compStructure[name]+portout;
                    }
                }
            if (class == "global")
                {   
                    // println(typeOf(<comp.ins>));
                    // for (i<-comp.ins)
                    //     {inputs = inputs + i; }
                        // println(inputs);
                    for (i<-comp.ins)
                    {
                        input = ("<i.name>":("type":"<i.typ>","unit":"<i.units>"));
                        portin["inputs"] =  portin["inputs"] + input;
                        // comps["glob"]["inputs"] = comps["glob"]["inputs"] + input;
                    }
                    // println("this is a global variable <compStructure>");
                    compStructure["glob"] = compStructure["glob"]+portin;
    
                }
        }else{println("Rename component and try again");}
}