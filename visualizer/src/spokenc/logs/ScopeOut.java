package spokenc.logs;

public class ScopeOut extends LogEntry {
	public ScopeOut(String fileName, int fileLine) {
		super(fileName, fileLine);
	}
	
	public String toString() {
		return super.toString() + ":scope_out";
	}
	
	public static String getDescriptor() {
		return "scope_out";
	}
}
