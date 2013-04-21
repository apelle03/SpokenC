package spokenc.logs.types;

public class StringValue extends Value {
	private String value;
	
	public StringValue() {
		this(null);
	}
	
	public StringValue(String value) {
		this.value = value;
	}
	
	public boolean hasValue() {
		return value != null;
	}
	
	public String getValue() {
		if (hasValue()) {
			return value;
		} else {
			return "undef";
		}
	}

	public void setValue(String value) {
		this.value = value;
	}

	public String toString() {
		return getValue();
	}
}
