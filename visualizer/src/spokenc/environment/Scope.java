package spokenc.environment;

import java.awt.Color;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import javax.swing.text.BadLocationException;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import javax.swing.text.StyledDocument;

public class Scope {
	protected String name;
	protected Map<String, Variable> variables;
	
	public Scope(String name) {
		this(name, null);
	}
	
	public Scope(String name, List<Variable> variables) {
		this.name = name;
		this.variables = new LinkedHashMap<>();
		if (variables != null) {
			for (Variable v : variables) {
				this.variables.put(v.getName(), v);
			}
		}
	}

	public String getName() {
		return name;
	}

	public List<Variable> getVariables() {
		return new ArrayList<Variable>(variables.values());
	}
	
	public void addVariable(Variable variable) {
		variables.put(variable.getName(), variable);
	}
	
	public Variable getVariable(String name) {
		return variables.get(name);
	}
	
	public boolean containsVariable(String name) {
		return variables.containsKey(name);
	}
	
	public String prettyPrint(String indent) {
		String str = "";
		for (Variable var : variables.values()) {
			str += indent + var.getName() + " = " + var.getValue() + "\n";
		}
		return str;
	}
	
	public void appendToStyledDocument(StyledDocument doc, Color color, String indent) {
		SimpleAttributeSet highlight = new SimpleAttributeSet();
		StyleConstants.setBackground(highlight, color);
		
		try {
			doc.insertString(doc.getLength(), prettyPrint(indent), highlight);
		} catch (BadLocationException e) {
			e.printStackTrace();
		}
	}
	
	public String toString() {
		String str = name + " {\n";
		for (Variable var : variables.values()) {
			str += "\t\t" + var.getName() + " = " + var.getValue() + "\n";
		}
		return str + "\t}";
		//return name + " " + variables.toString();
	}
}
