module IDE

import util::LanguageServer;
import util::Reflective;

import IO;
import ParseTree;

import Syntax;
import AST;
import CST2AST;



set[LanguageService] myLanguageContributor() = {
    parser(Tree (str input, loc src) {
        return parse(#start[Program], input, src);
    }),
    lenses(myLenses),
    executor(myCommands),
    summarizer(mySummarizer
        , providesDocumentation = true
        , providesDefinitions = true
        , providesReferences = false
        , providesImplementations = false)
};

data Command
  = compileOca(start[Program] form);

rel[loc,Command] myLenses(start[Program] input) 
  = {<input@\loc, compileOca(input)>};

void myCommands(compileOca(start[Program] oca)) {
    // compile(cst2ast(oca));
}

Summary mySummarizer(loc origin, start[Program] input) {
  println(input);
  Program ast = cst2ast(input);
//   RefGraph g = resolve(ast);
//   TEnv tenv = collect(ast);

//   set[Message] msgs = check(ast, tenv, g.useDef);

//   rel[loc, Message] msgMap = {< m.at, m> | Message m <- msgs };
  
//   rel[loc, str] docs = { <u, "Type: <type2str(t)>"> | <loc u, loc d> <- g.useDef, <d, _, _, Type t> <- tenv };
// return summary(origin, messages = msgMap, definitions = g.useDef, documentation = docs);
  return summary(origin);
}

void main() {
    registerLanguage(
        language(
            pathConfig(srcs = [|std:///|, |project://orchestra/src|]),
            "Orchestra",
            "oca",
            "IDE",
            "myLanguageContributor"
        )
    );
}


void load() {
    a = parsePrograms(|cwd:///examples/full_example.oca|);
    op = cst2ast(a.top);
    print(op);
}