package cs171.printf.logs.types;

public class VarValue {
	protected String name;
	protected VarType type;
	protected Value value;
	
	public VarValue(VarType type, String name) {
		this(type, name, null);
	}
	
	public VarValue(VarType type, String name, String value) {
		this.type = type;
		this.name = name;
		if (type == VarType._string || type == VarType._char || type == VarType._signed_char || type == VarType._unsigned_char) {
			this.value = new StringValue(value);
		} else {
			this.value = new IntegerValue(value);
		}
	}
	
	public String getType() {
		return type.toString();
	}

	public String getName() {
		return name;
	}
	
	public boolean hasValue() {
		return value.hasValue();
	}

	public String getValue() {
		return value.getValue();
	}

	public void setValue(Value value) {
		this.value = value;
	}
	
	public String toString() {
		if (value.hasValue()) {
			return getType() + "," + getName() + "," + getValue();
		} else {
			return getType() + "," + getName();
		}
	}
}
