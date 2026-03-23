#DT_sys
import src.Comm
import src.exeAreas
import src.GlOb
import time
import networkx as nx
import matplotlib.pyplot as plt

import threading

class MainManager:
    def __init__(self, exeAreas = [], globals = None, appTime = None):
        self.threads = []
        self.exeAreas = exeAreas
        self.globals = globals
        self.appTime = appTime
        self.globals.add_appTime(self.appTime)
        self.components = self.componentsExtract(self.exeAreas)
        self.graph = graphPlot(components = self.components, allcomponents = self.components, title = 'Service', printFlag = True)
    
         
    def startService(self):
        """Start the execution of areas using different threads in each area"""
        
        print('---------------------------------------------')
        print(f"Service execution has started")
        print('---------------------------------------------')
        self.initAreas()
        self.appTime.re_startApp()
        for area in self.exeAreas:
            self.start_thread(target=self.areaExec, args=(area,))  # Pass the method reference and the area as an argument
    
    def start_thread(self, target, args=()):
        thread = threading.Thread(target=target, args=args, daemon=True)
        self.threads.append(thread)
        thread.start()
    
    def initAreas(self):
        """Initialize all the areas components
        """
        for area in self.exeAreas:
            print('---------------------------------------------')
            print(f"{area.name} has been initialized")
            print('---------------------------------------------')
            area.initialize()
    
    def areaExec(self,area)->None:
        starttrigg = area.startTrigger
        t = 0
        while  self.globals.stopApp == False:
            if starttrigg.evaluate() == True:
            # if starttrigg.evaluate() == True or iter>6:
                print('\n')
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print(f"{area.name} has started its execution")
                print(f"{area.name} has time {t}")
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                area.execute()
                t += 5
                print('+++++++++++++++++++++++++++++++++++++++++++++')
                print(f"{area.name} has finished its execution")
                print('+++++++++++++++++++++++++++++++++++++++++++++')
                time.sleep(1)
    def join_threads(self):
        for thread in self.threads:
            thread.join()
    
    def componentsExtract (self,areas=[])->list:
        """_summary_

        Args:
            areas (list, optional): _description_. Defaults to [].

        Raises:
            ValueError: _description_

        Returns:
            list: _description_
        """
        components = []
        for area in areas:
            areacomponents =area.exeComponents
            for component in areacomponents:
                if component not in components:
                    components.append(component)
        return components
            


class graphPlot:
    
    def __init__(self, components = [], allcomponents = [], title = 'Directed Graph', printFlag = True):
        
        
        self.printFlag = printFlag
        self.components =components
        self.allcomponents =allcomponents
        
        self.relationships = self.relationAnalysis(components=self.components,allComponents=self.allcomponents)
        self.compColor = self.coloDef(components=self.components)
        # if type(assumtion) == str:
        #     self.assumtion = [assumtion]
        # elif type(assumtion) == list:
        #     self.assumtion = assumtion
        # else:
        #     print('Please intrudce the assumption as a list, even if it has only one element or as an empty list')
        #methods created for usage
        self.graph = self.create_directional_graph_wIndNodes(self.relationships)
        
        # self.sccs = self.tarjans_algorithm(self.graph)
        # self.cycleDetected = False
        
        
        # for group in self.sccs:
        #     if len(group) > 1:
        #         self.cycleDetected = True
        
        # if self.cycleDetected == False:
        #     self.topological_order = self.topological_sort(self.graph)
        #     self.new_graph = None
        #     self.cycle_topological_order = None
        #     self.cycleName= None
        # else:
        #     self.new_graph = self.create_scc_encapsulated_graph(self.graph,self.sccs)
        #     self.topological_order = self.topological_sort(self.new_graph)
        #     self.cycle_topological_order = self.sort_cycle(self.graph,self.sccs,self.assumtion)
        #     self.cycleName= self.findCycleName(self.topological_order)
        
        self.title = title
        if printFlag == True:
            self.plot_directed_graph_colors(self.graph,self.compColor)
    
    def __str__(self):
        message = "Scheduling order suggested for the simulation components." + '\n' "Order is: " + '\n'
        index = 0
        for comp in self.topological_order:
            index += 1
            message = message + str(index) + ':' + comp + '\n'
        if self.cycleDetected:
            cycle_message = 'There is a cycle and its name as a component is ' + str(self.cycleName) + " its components' order is:" + '\n'
            for comp in self.cycle_topological_order:
                cycle_message += comp + '\n'

    def coloDef (self,components)->dict:
        """_summary_

        Args:
            components (_type_): _description_

        Returns:
            dict: _description_
        """
        colors = {'Source':'tab:green','Model':'tab:blue','Config':'tab:olive','Sink':'tab:red','Others':'tab:gray'}
        compColor = {}
        for component in components:
            if type(component) == Comm.Source:
                compColor[component.name] = colors['Source']
            elif type(component) == Comm.Model:
                compColor[component.name] = colors['Model']
            elif type(component) == Comm.Sink:
                compColor[component.name] = colors['Sink']
            elif type(component) == Comm.ConfigComp:
                compColor[component.name] = colors['Config']
            else:
                compColor[component.name] = colors['Others']
        return compColor
    
    def relationAnalysis(self, components, allComponents) -> dict:
        """
        Analyze a set of components and generate a dictionary of dependencies.

        Args:
            components (list): The list of components to analyze.
            allComponents (list): The complete list of components in the system.

        Returns:
            dict: A dictionary mapping each component name to its dependencies.
                Components without dependencies or inports are mapped to an empty dictionary.
        """
        Alldependencies= {}
        allCompNames = {}
        areaCompNames = []
        for component in components:
            areaCompNames.append(component.name) 
        for component in allComponents:
            allCompNames[component.name] = component
        sizeDict = len(list(allCompNames.keys()))
        # if sizeDict != len(allComponents):
        #     print('All names in the system should be different, there are some repeated names')
        #     return 0
        if sizeDict != len(allComponents):
            raise ValueError("Duplicate names found in the system.")
        compFound =[]
        for component in components:
            dependsON ={}
            if component.inports == None:
                Alldependencies[component.name] = {}
            else:
                for inport,port in component.inports.items():
                    componentSrc =port.connector.src['component'].name
                    if componentSrc in dependsON.keys():
                        dependsON[componentSrc].append(port.name)
                    else:
                        dependsON[componentSrc]=[port.name]

                Alldependencies[component.name] = dependsON
            compfoundTemp = list(dependsON.keys())
            for comp in compfoundTemp:
                compFound.append(comp)
            
        flagRepeat = False
        
        for comp in compFound:
            if comp not in areaCompNames and allCompNames[comp].type in list(self.COMUNICATION_TYPES.keys()):
                flagRepeat = True
                components.append(allCompNames[comp])
        
        if flagRepeat == True:
            Alldependencies = self.relationAnalysis(components,allComponents)
        
        return Alldependencies
    
    def findCycleName(self, names)->list:
        cycleNames = []
        for name in names:
            if name.find('Cycle') != -1 :
                cycleNames.append(name)
        return cycleNames
    
    def create_directional_graph(self, relationship_dict) ->dict:
        directional_graph = {}

        for node, connections in relationship_dict.items():
            for target_node in connections:
                if target_node:
                    if target_node not in directional_graph:
                        directional_graph[target_node] = set()
                    directional_graph[target_node].add(node)
                if node not in directional_graph:
                    directional_graph[node] = set()

        return {node: list(edges) for node, edges in directional_graph.items()}
    
    def create_directional_graph_wIndNodes(self, relationship_dict):
        directional_graph = {}

        # Iterate through each node and its connections in the input dictionary
        for node, connections in relationship_dict.items():
            # Ensure the node itself is included in the directional graph
            if node not in directional_graph:
                directional_graph[node] = set()
            
            for target_node in connections:
                # Add the node to the adjacency list of the target node
                if target_node:
                    if target_node not in directional_graph:
                        directional_graph[target_node] = set()
                    directional_graph[target_node].add(node)

        # Add any nodes that are in the relationships as independent nodes if they are not present
        for node in relationship_dict:
            if node not in directional_graph:
                directional_graph[node] = set()

        # Convert sets to lists for consistency
        return {node: list(edges) for node, edges in directional_graph.items()} 
    
    def plot_directed_graph_colors(self, directional_graph, compColor={}):
    # Create a directed graph object
        G = nx.DiGraph()

        # Add nodes and edges from the directional graph dictionary
        for node, edges in directional_graph.items():
            for edge in edges:
                G.add_edge(node, edge)
            # Ensure the node itself is included in the graph
            if node not in G:
                G.add_node(node)

        # Ensure all nodes from the original graph are included, even if they have no edges
        all_nodes = set(directional_graph.keys())
        for node in all_nodes:
            if node not in G:
                G.add_node(node)

        # Draw the graph
        pos = nx.spring_layout(G)  # Position nodes using the spring layout
        plt.figure(figsize=(14, 7))
        
        # Use the compColor dictionary for node colors, defaulting to 'lightblue' if a node has no specified color
        node_colors = [compColor.get(node, "lightblue") for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color=node_colors, alpha=0.5, linewidths=5)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

        # Draw edges with arrows separately to ensure each direction is represented
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True, arrowstyle='-|>', 
                            arrowsize=20, edge_color="red", connectionstyle='arc3,rad=0.2')

        plt.title(self.title)
        plt.show()

    
    def plot_directed_graph_wIndNodes(self,directional_graph):
        # Create a directed graph object
        G = nx.DiGraph()

        # Add nodes and edges from the directional graph dictionary
        for node, edges in directional_graph.items():
            for edge in edges:
                G.add_edge(node, edge)
            # Ensure the node itself is included in the graph
            if node not in G:
                G.add_node(node)

        # Ensure all nodes from the original graph are included, even if they have no edges
        all_nodes = set(directional_graph.keys())
        for node in all_nodes:
            if node not in G:
                G.add_node(node)

        # Draw the graph
        pos = nx.spring_layout(G)  # Position nodes using the spring layout
        plt.figure(figsize=(14, 7))
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue", alpha=0.5, linewidths=5)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

        # Draw edges with arrows separately to ensure each direction is represented
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True, arrowstyle='-|>', 
                            arrowsize=20, edge_color="red", connectionstyle='arc3,rad=0.2')

        plt.title(self.title)
        # plt.title("Directed Graph")
        plt.show()
    
    def plot_bidirected_graph(self, directional_graph):
        # Create a directed graph object
        G = nx.DiGraph()

        # Add nodes and edges from the directional graph dictionary
        for node, edges in directional_graph.items():
            for edge in edges:
                G.add_edge(node, edge)

        # Draw the graph
        pos = nx.spring_layout(G)  # Position nodes using the spring layout
        plt.figure(figsize=(10, 6))
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", 
                font_size=10, font_weight="bold", edge_color="gray", arrows=True, 
                arrowstyle='-|>', arrowsize=20)

        plt.title("Directed Graph")
        plt.show()

    def plot_directed_graph(self, directional_graph):
        # Create a directed graph object
        G = nx.DiGraph()

        # Add nodes and edges from the directional graph dictionary
        for node, edges in directional_graph.items():
            for edge in edges:
                G.add_edge(node, edge)

        # Draw the graph
        pos = nx.spring_layout(G)  # Position nodes using the spring layout
        plt.figure(figsize=(15, 9))
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue", alpha= 0.5, linewidths=5)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

        # Draw edges with arrows separately to ensure each direction is represented
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True,arrowstyle='-|>', 
                            arrowsize=20, edge_color="red", connectionstyle='arc3,rad=0.2')

        plt.title("Directed Graph")
        plt.show()
   
    def tarjans_algorithm(self, directional_graph)->list:
        index = 0
        stack = []
        indices = {}
        lowlink = {}
        on_stack = {}
        sccs = []

        def strongconnect(node):
            nonlocal index
            indices[node] = index
            lowlink[node] = index
            index += 1
            stack.append(node)
            on_stack[node] = True

            for neighbor in directional_graph.get(node, []):
                if neighbor not in indices:
                    strongconnect(neighbor)
                    lowlink[node] = min(lowlink[node], lowlink[neighbor])
                elif on_stack[neighbor]:
                    lowlink[node] = min(lowlink[node], indices[neighbor])

            if lowlink[node] == indices[node]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    scc.append(w)
                    if w == node:
                        break
                sccs.append(scc)

        for node in directional_graph:
            if node not in indices:
                strongconnect(node)
        return sccs
    
    def topological_sort(self, directional_graph)->list:
        visited = set()
        stack = []

        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for neighbor in directional_graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(node)

        for node in directional_graph:
            if node not in visited:
                dfs(node)

        return stack[::-1]
    
    def create_scc_encapsulated_graph(self,directional_graph, sccs)->dict:
        # Create a mapping from nodes to their SCC index
        node_to_scc = {}
        for idx, scc in enumerate(sccs):
            for node in scc:
                node_to_scc[node] = f"Cycle{idx}" if len(scc) > 1 else node
        
        # Initialize the new graph
        new_graph = {scc_id: set() for scc_id in node_to_scc.values()}

        # Populate the new graph
        for node, neighbors in directional_graph.items():
            node_scc = node_to_scc[node]
            for neighbor in neighbors:
                neighbor_scc = node_to_scc[neighbor]
                if node_scc != neighbor_scc:
                    new_graph[node_scc].add(neighbor_scc)

        # Convert sets to lists for consistency
        new_graph = {k: list(v) for k, v in new_graph.items()}

        return new_graph
    
    def sort_cycle(self, directional_graph,sccs,assumption)->list:
        if assumption == []:
            assumption = list(self.relationships.keys())[0]
        else:
            assumption = assumption[0]
            
        for group in sccs:
            if len(group) != 1:
                cycle_comp = group
        cycle_directional_graph = {}
        for name, dependencies in directional_graph.items():
            new_dependency = []
            for comp in dependencies:
                if comp != assumption and comp in cycle_comp:
                    new_dependency.append(comp)
            if name in cycle_comp:
                cycle_directional_graph[name] = new_dependency
        
                
        cycle_order = self.topological_sort(cycle_directional_graph)
        # print(cycle_directional_graph)
        return(cycle_order)

    
    
    
    



                 


                 
class Comp_manager:
    
    COMPONENT_TYPES = {'sen': 'Sensor', 'mod': 'Model', 'op': 'Operation', 'agg': 'Aggreggator',
                       'dup': 'Dupplicator','spl': 'Splitter','conn': 'Connector','swi': 'Switch', 
                       'inp': 'Input port', 'outp': 'Output port' }
    
    def __init__(self, service_name = "name") -> None:
        self.service_name = service_name
        self.components = {'sen': [], 'mod': [], 'op': [], 'agg': [],
                       'dup': [],'spl': [],'conn': [],'swi': [], 
                       'inp': [], 'outp': [] }
        self.comp_names = {}
        
    def component_agreggate(self, comp_name = 'name', compt_type = 'mod'):
        '''
        Aggreggates components of the whole system, generate a unique ID and correlates the ID with 
        a component name (names can be the same between components, but not IDs)
        we assume that 2 components of the same type do not have the same name, 
        otherwise problems might rise
        '''
        comp_list = self.components[compt_type]
        comp_ID = str(compt_type) + str(len(comp_list) + 1)
        
        self.comp_names[comp_ID] = comp_name
        self.components[compt_type].append(comp_ID)
        #generate the component object
        # comp_ID = DSL_semantics.Component(comp_name, comp_ID)
