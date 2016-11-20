package kr.swmaestro.swmaestro.data;

import org.json.JSONException;
import org.json.JSONObject;

public class DataLogin {
	private JSONObject mJsonObject;
	
	public DataLogin(JSONObject jsonObject){
		mJsonObject = jsonObject;
	}
	
	public String getSessionKey(){
		try {
			return mJsonObject.getString("session_key");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public JSONObject getUserDataJsonObject(){
		try {
			return mJsonObject.getJSONObject("user_data");
		} catch (JSONException e) {
			e.printStackTrace();
			return null;
		}
	}
}
