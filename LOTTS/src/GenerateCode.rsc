module GenerateCode

import IO;
import LOTTS2;
import String;


str generateComponents(Service s) {
    str code = "";
    visit(s) {
        case Sensor(_, Id name, outs):
            code += generateSensorPython(name, outs);
        case UX(_, Id name, ins, outs):
            code += generateUXPython(name, ins, outs);
        case Dataprocess(_, Id name, ins, outs):
            code += generateDataProcessPython(name, ins, outs);
        case Model(_, Id name, ins, outs, config):
            code += generateModelPython(name, ins, outs, config);
        case Duplicator(_, Id name, inPort, outs):
            code += generateDuplicatorPython(name, inPort, outs);
        case Transformation(_, Id name, ins, outs, defs):
            code += generateTransformPython(name, ins, outs, defs);
        case Aggregator(_, Id name, ins, out):
            code += generateAggregatorPython(name, ins, out);
        case Splitter(_, Id name, inPort, outs):
            code += generateSplitterPython(name, inPort, outs);
        case Switch(_, Id name, ins, out, defExp):
            code += generateSwitchPython(name, ins, out, defExp);
    }
    return code;
}

str generateSensorPython(str name, list[Port] outs) {
    str code = genOutputs(outs) + name + " = Comm.Source(name='" + name + "', outputs=outputs)\n\n";
    return code;
}

str generateUXPython(str name, list[Port] ins, list[Port] outs) {
    str code = genInputs(ins) + name + " = Comm.Sink(name='" + name + "', inputs=inputs)\n\n";
    return code;
}

str generateDataProcessPython(str name, list[Port] ins, list[Port] outs) {
    return genInputsOutputs(ins, outs) + name + " = Comm.Model(name='" + name + "', SimE='Python', modelDir=directory, inputs=inputs, outputs=outputs, parameters=[])\n\n";
}

str generateModelPython(str name, list[Port] ins, list[Port] outs, list[EspecialExp] config) {
    str code = genInputsOutputs(ins, outs);
    str params = "[" + join([genConfigParam(e) | EspecialExp e <- config], ", ") + "]";
    code += name + " = Comm.Model(name='" + name + "', SimE='FMU', modelDir=directory, inputs=inputs, outputs=outputs, parameters=" + params + ")\n\n";
    return code;
}

str generateDuplicatorPython(str name, Port inPort, list[Port] outs) {
    return genInput(inPort) + name + " = Comm.Duplicator(input=input, num_outputs=" + toString(size(outs)) + ")\n\n";
}

str generateTransformPython(str name, list[Port] ins, list[Port] outs, list[Expression] defs) {
    str code = genInputsOutputs(ins, outs);
    code += "exp = '" + join([toString(e) | e <- defs], "; ") + "'\nvars = {}\n";
    code += name + " = Comm.Transformation(outputs=outputs, inputs=inputs, expressions=exp, variables=vars)\n\n";
    return code;
}

str generateAggregatorPython(str name, list[Port] ins, Port out) {
    return genInputs(ins) + genOutput(out) + name + " = Comm.Aggregator(inputs=inputs, output=output)\n\n";
}

str generateSplitterPython(str name, Port inPort, list[Port] outs) {
    return genInput(inPort) + genOutputs(outs) + name + " = Comm.Splitter(input=input, outputs=outputs)\n\n";
}

str generateSwitchPython(str name, list[Port] ins, Port out, EspecialExp defExp) {
    return genInputs(ins) + genOutput(out) + "condition = '" + toString(defExp) + "'\n" + name + " = Comm.Switch(inputs=inputs, output=output, condition=condition)\n\n";
}

str genInputs(list[Port] ins) {
    return join([genInput(p) | p <- ins], "") + "inputs = [" + join(["input" | _ <- ins], ", ") + "]\n";
}

str genOutputs(list[Port] outs) {
    return join([genOutput(p) | p <- outs], "") + "outputs = [" + join(["output" | _ <- outs], ", ") + "]\n";
}

str genInputsOutputs(list[Port] ins, list[Port] outs) {
    return genInputs(ins) + genOutputs(outs);
}

str genInput(Port(typ, name, units)) {
    return "input = {'name': '" + name + "', 'unit': '" + flattenUnit(units) + "', 'datatype': '" + typ + "', 'val': ''}\n";
}

str genOutput(Port(typ, name, units)) {
    return "output = {'name': '" + name + "', 'unit': '" + flattenUnit(units) + "', 'datatype': '" + typ + "', 'val': ''}\n";
}

str genConfigParam(EspecialExp(assign(Id id, LiteralExpression le, Unit u))) {
    return "{'name': '" + id + "', 'unit': '" + flattenUnit([u]) + "', 'datatype': 'float', 'val': '" + toString(le) + "'}";
}

str generateConnections(Service s) {
    str code = "\nconnections = exeMgn.ConnectionHandler()\n";
    visit(s) {
        case Connector(_, Id name, Id srcComp, Id outPort, Id dstComp, Id inPort, ExchMethod ex):
            code += "connections.connect(source={'component': " + srcComp + ", 'output': '" + outPort + "'}, ";
            code += "destination={'component': " + dstComp + ", 'input': '" + inPort + "'}, ";
            code += "exPattern={'type': '" + showExch(ex) + "'})\n";
    }
    return code;
}

str generateExecutionAreas(Service s) {
    return "# Execution manager generation here\n";
}

str flattenUnit(list[Unit] units) {
    return join([u | BasicUnit u <- units], " ");
}

str showExch(ExchMethod ex) {
    switch (ex) {
        case fifo: return "FIFO";
        case lifo: return "LIFO";
        case lvq: return "LVQ";
        case pq: return "PQ";
    }
    return "FIFO";
}
