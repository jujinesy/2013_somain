package kr.swmaestro.swmaestro.data;

import org.json.JSONException;
import org.json.JSONObject;

public class DataNotice {
	private JSONObject mJsonobject;
	
	public DataNotice(JSONObject jsonObject){
		mJsonobject = jsonObject;
	}
	
	public String getCategory(){
		try {
			return mJsonobject.getString("category");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getTitle(){
		try {
			return mJsonobject.getString("title");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getContent(){
		try {
			return mJsonobject.getString("content");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getCreatedDate(){
		try {
			return mJsonobject.getString("created_day");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getCreatedTime(){
		try {
			return mJsonobject.getString("created_time");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
}
