package cs171.printf.environment;

import javax.swing.text.StyledDocument;

import cs171.printf.logs.types.VarValue;

public class Variable {
	public static int NumDecls = 0;
	public static int NumLines = 0;
	
	protected int declNum;
	protected int logLine;
	protected VarValue value;
	
	protected String function;
	protected StyledDocument callStack;
	
	public Variable(VarValue value, String function) {
		this(value, function, NumDecls++);
	}
	
	public Variable(VarValue value, String function, int declNum) {
		this(value, function, declNum, NumLines++);
	}
	
	private Variable(VarValue value, String function, int declNum, int logLine) {
		this.value = value;
		this.declNum = declNum;
		this.logLine = logLine;
		this.function = function;
		this.callStack = null;
	}
	
	public String getType() {
		return value.getType();
	}
	
	public String getName() {
		return value.getName();
	}
	
	public String getValue() {
		return value.getValue();
	}
	
	public String getFunction() {
		return function;
	}
		
	public StyledDocument getCallStack() {
		return callStack;
	}
	
	public void setCallStack(StyledDocument callStack) {
		this.callStack = callStack;
	}

	public int getDeclNum() {
		return declNum;
	}

	public int getLogLine() {
		return logLine;
	}

	public String toString() {
		if (value.hasValue()) {
			return value.getValue();
		} else {
			return value.getName();
		}
	}
}
