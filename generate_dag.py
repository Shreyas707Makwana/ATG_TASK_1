import os
from graphviz import Digraph


def generate_dag_visualization(output_path: str = "debate_dag"):
    dot = Digraph(comment='Multi-Agent Debate DAG', format='png')
    dot.attr(rankdir='TB')
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')
    
    dot.node('UserInput', 'UserInputNode\n(Get Topic)', fillcolor='lightgreen')
    dot.node('Coordinator', 'CoordinatorNode\n(Turn Control)', fillcolor='lightyellow')
    dot.node('AgentA', 'AgentA Node\n(Scientist)', fillcolor='lightcoral')
    dot.node('AgentB', 'AgentB Node\n(Philosopher)', fillcolor='lightcoral')
    dot.node('Memory', 'MemoryNode\n(Store Arguments)', fillcolor='lightcyan')
    dot.node('Logger', 'LoggerNode\n(Log Everything)', fillcolor='lavender')
    dot.node('Judge', 'JudgeNode\n(Evaluate & Decide)', fillcolor='lightgoldenrod')
    dot.node('END', 'END', shape='doublecircle', fillcolor='pink')
    
    dot.edge('UserInput', 'Coordinator', label='topic')
    dot.edge('Coordinator', 'AgentA', label='if AgentA turn')
    dot.edge('Coordinator', 'AgentB', label='if AgentB turn')
    dot.edge('Coordinator', 'Judge', label='if round 8 complete')
    
    dot.edge('AgentA', 'Memory', label='argument')
    dot.edge('AgentB', 'Memory', label='argument')
    
    dot.edge('Memory', 'Logger', label='updated memory')
    dot.edge('Logger', 'Coordinator', label='next round', constraint='false')
    
    dot.edge('Judge', 'Logger', label='verdict')
    dot.edge('Logger', 'END', label='complete')
    
    with dot.subgraph(name='cluster_legend') as c:
        c.attr(label='Legend', style='dashed')
        c.node('leg1', 'Input Node', fillcolor='lightgreen')
        c.node('leg2', 'Control Node', fillcolor='lightyellow')
        c.node('leg3', 'Agent Node', fillcolor='lightcoral')
        c.node('leg4', 'Storage Node', fillcolor='lightcyan')
        c.node('leg5', 'Evaluation Node', fillcolor='lightgoldenrod')
        c.node('leg6', 'Utility Node', fillcolor='lavender')
    
    try:
        dot.render(output_path, cleanup=True)
        print(f"✓ DAG visualization saved to: {output_path}.png")
        
        dot.format = 'svg'
        dot.render(output_path, cleanup=True)
        print(f"✓ DAG visualization saved to: {output_path}.svg")
        
        return True
    except Exception as e:
        print(f"✗ Error generating DAG visualization: {e}")
        print("  Make sure Graphviz is installed: https://graphviz.org/download/")
        return False


def generate_detailed_dag():
    dot = Digraph(comment='Detailed Debate Flow', format='png')
    dot.attr(rankdir='LR')
    dot.attr('node', shape='box', style='filled', fillcolor='lightblue')
    
    dot.node('start', 'START\n(Get Topic)', shape='ellipse', fillcolor='lightgreen')
    
    for round_num in range(1, 9):
        agent = 'A' if round_num % 2 == 1 else 'B'
        node_id = f'round{round_num}'
        
        label = f'Round {round_num}\nAgent{agent}\n↓\nMemory\n↓\nLogger'
        color = 'lightcoral' if agent == 'A' else 'lightsalmon'
        
        dot.node(node_id, label, fillcolor=color)
        
        if round_num == 1:
            dot.edge('start', node_id)
        else:
            dot.edge(f'round{round_num-1}', node_id)
    
    dot.node('judge', 'JudgeNode\nEvaluate\nDetermine Winner', fillcolor='lightgoldenrod')
    dot.edge('round8', 'judge')
    
    dot.node('end', 'END\n(Output Results)', shape='ellipse', fillcolor='pink')
    dot.edge('judge', 'end')
    
    try:
        dot.render('debate_dag_detailed', cleanup=True)
        print(f"✓ Detailed DAG visualization saved to: debate_dag_detailed.png")
        return True
    except Exception as e:
        print(f"✗ Error generating detailed DAG: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("DAG Visualization Generator")
    print("="*60 + "\n")
    
    success1 = generate_dag_visualization()
    
    print()
    
    success2 = generate_detailed_dag()
    
    print("\n" + "="*60)
    if success1 or success2:
        print("✓ DAG generation completed!")
    else:
        print("✗ DAG generation failed. Install Graphviz:")
        print("  Windows: https://graphviz.org/download/")
        print("  Linux: sudo apt-get install graphviz")
        print("  Mac: brew install graphviz")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()