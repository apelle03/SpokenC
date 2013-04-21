package cs171.printf.environment;

import java.awt.Color;
import java.util.ArrayList;
import java.util.Stack;

import javax.swing.text.BadLocationException;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import javax.swing.text.StyledDocument;

public class FunctionScope {
	protected String name;
	protected Stack<Scope> subscopes;
	protected int numScopes;
	
	public FunctionScope(String name) {
		this.name = name;
		numScopes = 0;
		subscopes = new Stack<>();
		scopeIn();
	}
	
	public String getName() {
		return name;
	}
	
	public void scopeIn() {
		subscopes.push(new Scope(name + ":" + numScopes++));
	}
	
	public void scopeOut() {
		if (numScopes > 0) {
			subscopes.pop();
			numScopes--;
		}
	}
	
	public Scope getScope() {
		return subscopes.peek();
	}
	
	private Scope getEnclosingScope(String name) {
		Scope scopes[] = new Scope[numScopes];
		scopes = subscopes.toArray(scopes);
		for (int i = numScopes - 1; i >= 0; i--) {
			if (scopes[i].containsVariable(name)) {
				return scopes[i];
			}
		}
		return null;
	}
	
	public void addVariable(Variable variable) {
		getScope().addVariable(variable);
	}
	
	public void updateVariable(Variable variable) {
		Scope scope = getEnclosingScope(variable.getName());
		if (scope != null) {
			scope.addVariable(variable);
		}
	}
	
	public Variable getVariable(String name) {
		Scope scope = getEnclosingScope(name);
		if (scope != null) {
			return scope.getVariable(name);
		} else {
			return null;
		}
	}
	
	public boolean containsVariable(String name) {
		return getEnclosingScope(name) != null;
	}
	
	public void appendToStyledDocument(StyledDocument doc, Color color) {
		SimpleAttributeSet highlight = new SimpleAttributeSet();
		StyleConstants.setBackground(highlight, color);
		
		Scope[] scopes = new Scope[subscopes.size()];
		scopes = subscopes.toArray(scopes);
		
		String indent = "";
		String stackText = name + " {\n";
		for (int i = 0; i < scopes.length; i++) {
			indent += "  ";
			stackText += scopes[i].prettyPrint(indent);
		}
		int longest = 0;
		for (String line : stackText.split("\n")) {
			if (line.length() > longest) {
				longest = line.length();
			}
		}
		longest += 2;
		
		try {
			doc.insertString(doc.getLength(), padRight(name + " {", longest) + "\n", highlight);
			
			ArrayList<Color> scopeColors = new ArrayList<>();
			scopeColors.add(color);
			scopeColors.add(color);
			for (int i = 0; i < scopes.length; i++) {
				for (Variable var : scopes[i].getVariables()) {
					for (int j = 0; j < i + 1; j++) {
						StyleConstants.setBackground(highlight, scopeColors.get(j));
						doc.insertString(doc.getLength(), "  ", highlight);
					}
					StyleConstants.setBackground(highlight, scopeColors.get(i + 1));
					doc.insertString(doc.getLength(),
									 padRight(var.getName() + " = " + var.getValue(), longest - 2 * (i + 1)) + "\n",
									 highlight);
				}
				scopeColors.add(new Color((int)(scopeColors.get(i).getRed()   * .85),
		  				  (int)(scopeColors.get(i).getGreen() * .85),
		  				  (int)(scopeColors.get(i).getBlue()  * .85)));
			}
			StyleConstants.setBackground(highlight, color);
			doc.insertString(doc.getLength(), padRight("}", longest) + "\n", highlight);
		} catch (BadLocationException e) {
			e.printStackTrace();
		}
	}
	
	private String padRight(String str, int length) {
		return String.format("%1$-" + length + "s", str);
	}
	
	public String toString() {
		Scope[] scopes = new Scope[subscopes.size()];
		scopes = subscopes.toArray(scopes);
		String s = name + " {\n";
		String tabs = "";
		for (int i = 0; i < scopes.length; i++) {
			tabs += "  ";
			s += scopes[i].prettyPrint(tabs);
		}
		s += "}";
		return s;
	}
}
