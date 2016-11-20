package kr.swmaestro.swmaestro.data;

public class DataDocumentExtend {
	private String key;
	private String value;
	
	public DataDocumentExtend(String key, String value){
		this.key = key;
		this.value = value;
	}
	
	public String getKey(){
		return this.key;
	}
	
	public String getValue(){
		return this.value;
	}
}
