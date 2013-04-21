package cs171.printf.logs;

public class FuncCall extends LogEntry {
	private String funcName;
	
	public FuncCall(String fileName, int fileLine, String funcName) {
		super(fileName, fileLine);
		this.funcName = funcName;
	}

	public String getFuncName() {
		return funcName;
	}

	public void setFuncName(String funcName) {
		this.funcName = funcName;
	}
	
	public String toString() {
		return super.toString() + ":call(" + funcName + ")";
	}
	
	public static String getDescriptor() {
		return "call";
	}
}
