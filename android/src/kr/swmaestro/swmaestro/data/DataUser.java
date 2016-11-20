package kr.swmaestro.swmaestro.data;

import org.json.JSONException;
import org.json.JSONObject;


public class DataUser {
	private JSONObject mJsonObject;
	
	public DataUser(JSONObject jsonObject){
		mJsonObject = jsonObject;
	}
	public DataUser(String strJsonObject){
		try {
			mJsonObject = new JSONObject(strJsonObject);
		} catch (JSONException e) {
			e.printStackTrace();
		}
	}
	public DataUser(){
		mJsonObject = new JSONObject();
	}
	
	public String getUserName(){
		try {
			return mJsonObject.getString("username");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getUrlPhoto(){
		try {
			return mJsonObject.getString("photo");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getCourseStatus(){
		try {
			return mJsonObject.getString("course_status");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getCourseTerm(){
		try {
			return mJsonObject.getString("course_term");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getCourseStep(){
		try {
			return mJsonObject.getString("course_step");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getCourseDescription(){
		try {
			return mJsonObject.getString("course_description");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getBirthday(){
		try {
			return mJsonObject.getString("birthday");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getName(){
		try {
			return mJsonObject.getString("name");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public String getGender(){
		try {
			return mJsonObject.getString("gender");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
	
	public int getAge(){
		try {
			return mJsonObject.getInt("age");
		} catch (JSONException e) {
			e.printStackTrace();
			return 0;
		}
	}
	
	public String getType(){
		try {
			return mJsonObject.getString("type");
		} catch (JSONException e) {
			e.printStackTrace();
			return "";
		}
	}
}
