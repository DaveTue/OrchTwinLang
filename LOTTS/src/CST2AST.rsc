module CST2AST

import IO;
import Syntax;
import AST;
import ParseTree;

Program cst2ast(start[Program] sf) {
  Program f = sf.top; // remove layout before and after form
  println(f);
//   switch(f) {
  	// case (Resource)`resource <Id id> { <{MachineImage ","}+ imgs>}`: {
  	// 	return resource(cst2ast(id), [ cst2ast(image) | MachineImage image <- imgs ]);
  	// }
//   }
      return sensor(sensor("",units3("", [])));
}