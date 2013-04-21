package cs171.printf.logs;

import cs171.printf.logs.types.VarType;
import cs171.printf.logs.types.VarValue;

public class VarDeclaration extends LogEntry {
	protected VarValue value;
	
	public VarDeclaration(String fileName, int fileLine, VarValue value) {
		super(fileName, fileLine);
		this.value = value;
	}
	
	public VarDeclaration(String fileName, int fileLine, VarType type, String name, String value) {
		super(fileName, fileLine);
		this.value = new VarValue(type, name, value);
	}
	
	public VarValue getValue() {
		return value;
	}

	public void setValue(VarValue value) {
		this.value = value;
	}

	public String toString() {
		return super.toString() + ":decl(" + value.toString() + ")";
	}
	
	public static String getDescriptor() {
		return "decl";
	}
}
