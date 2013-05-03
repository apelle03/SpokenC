package spokenc.logs.types;

import java.math.BigInteger;

public class IntegerValue extends Value {
	private BigInteger value;
	
	public IntegerValue() {
		this(null);
	}
	
	public IntegerValue(String value) {
		this(value, 10);
	}
	
	public IntegerValue(String value, int radix) {
		if (value != null) {
			this.value = new BigInteger(value, radix);
		} else {
			this.value = null;
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

	public void setValue(String value) {
		this.value = new BigInteger(value);
	}

	public String toString() {
		return getValue();
	}
}
