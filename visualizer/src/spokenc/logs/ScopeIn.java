package spokenc.logs;

public class ScopeIn extends LogEntry {
	public ScopeIn(String fileName, int fileLine) {
		super(fileName, fileLine);
	}
	
	public String toString() {
		return super.toString() + ":scope_in";
	}
	
	public static String getDescriptor() {
		return "scope_in";
	}
}
