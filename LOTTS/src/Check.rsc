module Check

import IO;
import Syntax;
import ParseTree;

// ASensor implodeSensor(Tree parsetree) {
//   sensorAST = implode(#ASensor, parsetree);
//   println("RESULT: <checkWellformedness(sensorAST)>");
//   return sensorAST;
// }

Tree parseProgram(loc l) = parse(#start[Program], l);

bool loadAndCheck(loc c) {
  
  Tree tree = parseProgram(c);
  
  return checkWellformedness(tree.top);
  
}

bool checkWellformedness(Program p) {
  switch(p) {
    case (Program)`<Component c>`: return checkWellformedness(c);
    //case (Program)`<Sensor s>`: return checkWellformedness(s);
    case (Program)`<Program p1> <Program p2>`: return checkWellformedness(p1) && checkWellformedness(p2);
  }
  return true;
}

bool checkWellformedness((Component)`model : <Id modelName> <InputOutputDecl* ios>`){
  println("model");
  return true;
}

bool checkWellformedness((Component)`UX : <Id modelName> <InputOutputDecl* ios>`){
  println("UX");
  return true;
}

bool checkWellformedness((Component)`aggregator : <Id modelName> <InputOutputDecl* ios>`){
  println("aggregator <modelName>");
  int_count = 0;
  out_count = 0;
  for (io <- ios)  {
    
    switch(io){
      case(InputOutputDecl)`input : <InputOutputDecl inp>`: int_count+=1;
      case(InputOutputDecl)`output : <InputOutputDecl outp>`: out_count+=1;
    }
  }
  if (out_count > 1) {
    println("<modelName> should have only one output");
    return false;
  }else {return true;}
  
}

bool checkWellformedness((Component)`duplicator : <Id modelName> <InputOutputDecl* ios>`){
  println("duplicator");
  return true;
}

bool checkWellformedness((Component)`switch : <Id modelName> <InputOutputDecl* ios> <Behaviour b>`){
  println("switch");
  int_count = 0;
  out_count = 0;
  for (io <- ios)  {
    
    switch(io){
      case(InputOutputDecl)`input : <InputOutputDecl inp>`: int_count+=1;
      case(InputOutputDecl)`output : <InputOutputDecl outp>`: out_count+=1;
    }
  }
  if (out_count > 1) {
    println("<modelName> should have only one output");
    return false;
  }else {return true;}
  
}

bool checkWellformedness((Component)`splitter : <Id modelName> <InputOutputDecl* ios>`){
  println("splitter");
  int_count = 0;
  out_count = 0;
  for (io <- ios)  {
    
    switch(io){
      case(InputOutputDecl)`input : <InputOutputDecl inp>`: int_count+=1;
      case(InputOutputDecl)`output : <InputOutputDecl outp>`: out_count+=1;
    }
  }
  if (int_count > 1) {
    println("<modelName> should have only one input");
    return false;
  }else {return true;}
}

bool checkWellformedness((Component)`operation : <Id? modelName> <InputOutputDecl* ios> <Behaviour b>`){
  println("operation");
  return true;
}

bool checkWellformedness((Component)`connect : <Id id> <Def d> <Exchange e> <Transformation t>`){
  println("Connect <id>");
  return true;
}

bool checkWellformedness((Sensor)`sensor :<Id id> <InputOutputDecl out>`){
  println("sensor");
  println("<id> <out>");
  int_count = 0;
  out_count = 0;
  for (io <- out)  {
    
    switch(io){
      case(InputOutputDecl)`output : <InputOutputDecl outp>`: out_count+=1;
    }
  }
  if (out_count > 1) {
    println("<id> should have only one output");
    return false;
  }else
  {return true;}
}



/**
* This function checks all the elements in the parsetree
*/
// bool checkWellformedness(AProgram program) {
//   bool rta = true;
//   visit(program) {
//     case component(Component c): rta = rta && checkWellformedness(c);
//     case sensor(Sensor s): rta = rta && checkWellformedness(s);
//     case phrases(Program l, Program r): {
//       bool tmp = checkWellformedness(l) && checkWellformedness(r);
//       rta = rta && tmp;
//     }
//   }
//   return rta;
// }

// bool checkWellformedness(??) {
//   if (output(_) := out){
//     return true;
//   }
//   else {
//     return false;
//   }
// }

// Program implodeProgram(Tree parsetree) {
//   return implode(#ProgramExp, parsetree);
// }

// check Sensor
//  only output
//  1 function per langauge construct


// after checking

// mapping from AST -> Python


