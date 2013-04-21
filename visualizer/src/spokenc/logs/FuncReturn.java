package spokenc.logs;

import spokenc.logs.types.VarType;
import spokenc.logs.types.VarValue;

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
