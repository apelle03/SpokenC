package cs171.printf.logs;

import cs171.printf.logs.types.VarType;
import cs171.printf.logs.types.VarValue;

public class FuncReturn extends LogEntry {
	private String funcName;
	private VarValue value;
	
	public FuncReturn(String fileName, int fileLine, String funcName, VarValue value) {
		super(fileName, fileLine);
		this.funcName = funcName;
		this.value = value;
	}
	
	public FuncReturn(String fileName, int fileLine, String funcName, VarType type, String value) {
		super(fileName, fileLine);
		this.funcName = funcName;
		this.value = new VarValue(type, "ret", value);
	}
	
	public String getFuncName() {
		return funcName;
	}

	public void setFuncName(String funcName) {
		this.funcName = funcName;
	}

	public VarValue getValue() {
		return value;
	}

	public void setValue(VarValue value) {
		this.value = value;
	}

	public String toString() {
		return super.toString() + ":return(" + funcName + "," + value.toString() + ")";
	}
	
	public static String getDescriptor() {
		return "return";
	}
}
