package spokenc.logs.types;

public class FloatValue extends Value {
	private Double value;

	public FloatValue() {
		this(null);
	}
	
	public FloatValue(String value) {
		if (value == null) {
			this.value = null;
		} else {
			this.value = Double.parseDouble(value);
		}
	}
	
	public boolean hasValue() {
		return value != null;
	}

	public String getValue() {
		if (hasValue()) {
			return value.toString();
		} else {
			return "undef";
		}
	}
	
	public String toString() {
		return getValue();
	}	
}
