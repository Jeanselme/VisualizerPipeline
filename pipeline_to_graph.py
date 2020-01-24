"""
    Produce a graph from json pipeline
"""
import json
from rendering import buildGraph

class Step:
    """ 
        Tree structure used for the eclat algorithm
    """

    # Id of the given Node
    idNum = 0

    def __init__(self, name):
        """     
            Arguments:
                name {str} -- Name of the feature
                graph {graph object} -- To Display
        """

        self.name = name
        self.children = []
        self.id = Step.idNum
        Step.idNum += 1

    def addChild(self, child, arg_type):
        if child is not None:
            self.children.append((arg_type, child))

    def __str__(self, move = 0, mainBranch = False):
        string = "| " * move + " + Step : {} \n".format(self.name)
        for _, child in self.children:
            string += child.__str__(move + 1, mainBranch)
            if mainBranch:
                # Main branch only look at the first child
                break
        return string
    
class Pipeline:
    """
        DAG with extra information
    """
 
    def __init__(self, filename):
        """
            Reads the json and creates the associated pipeline
            Arguments:
                filename {str} -- File name
        """
        with open(filename) as pipeline:
            pipeline = json.load(pipeline) 
            
            self.id = pipeline['id']
            self.dag = self.extractSteps(pipeline['steps'])
                   
    def extractSteps(self, steps):
        """
            Extracts steps
        
            Arguments:
                steps {dict} -- Dictionary of primitives
        """
        extracted_step = []
        # Iterate over steps
        for step in steps:
            if "primitive" in step:
                # Extracts name (only most meaningful part)
                new_step = Step(step["primitive"]["python_path"].split('.')[3])
                extracted_step.append(new_step)
                
                # If have arguments in previous step, update the link between node
                if "arguments" in step:
                    for arg_type in step["arguments"]:
                        parent = step["arguments"][arg_type]["data"].split('.')
                        if parent[0] == "steps":
                            extracted_step[int(parent[1])].addChild(new_step, arg_type)
                        
        return extracted_step[0]
    
    def visualize(self):
        """
            Visualization of the dag
        """
        return buildGraph(self.dag)