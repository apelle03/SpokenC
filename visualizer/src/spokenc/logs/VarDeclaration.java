package spokenc.logs;

import spokenc.logs.types.VarType;
import spokenc.logs.types.VarValue;

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
