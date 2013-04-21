package cs171.printf.logs.types;

public enum VarType {
	_char			("char"),
	_signed_char	("signed char"),
	_unsigned_char	("unsigned char"),
	_string			("char*"),
	
	_short					("short"),
	_unsigned_short			("unsigned short"),
	_int					("int"),
	_unsigned_int			("unsigned int"),
	_long					("long"),
	_unsigned_long			("unsigned long"),
	_long_long				("long long"),
	_unsigned_long_long		("unsigned long long"),
	
	_int8_t		("int8_t"),
	_uint8_t	("uint8_t"),
	_int16_t	("int16_t"),
	_uint16_t	("uint16_t"),
	_int32_t	("int32_t"),
	_uint32_t	("uint32_t"),
	_int64_t	("int64_t"),
	_uint64_t	("uint64_t"),
	
	_pointer	("*");
	
	private String text;
	VarType(String text) {
		this.text = text;
	}

	public String toString() {
		return this.text;
	}

	public static VarType fromString(String text) {
		if (text != null) {
			for (VarType type : VarType.values()) {
				if (text.equalsIgnoreCase(type.text)) {
					return type;
				}
			}
		}
		return null;
	}
}
