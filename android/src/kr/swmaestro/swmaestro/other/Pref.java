package kr.swmaestro.swmaestro.other;

import java.util.ArrayList;

import kr.swmaestro.swmaestro.data.DataDocument;
import kr.swmaestro.swmaestro.data.DataLogin;
import kr.swmaestro.swmaestro.data.DataNotice;
import kr.swmaestro.swmaestro.data.DataUser;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.content.Context;
import android.content.SharedPreferences;

public class Pref {
	public static void removeSettingData(Context context){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		SharedPreferences.Editor editor = pref.edit();
		editor.clear();
		editor.commit();
	}
	
	public static void setAutoLogin(Context context, boolean isAutoLogin){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		SharedPreferences.Editor editor = pref.edit();
		editor.putBoolean("autoLogin", isAutoLogin);
		editor.commit();
	}
	public static boolean getAutoLogin(Context context){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		boolean value = pref.getBoolean("autoLogin", false);
		return value;
	}
	public static void setIdPw(Context context, String id, String pw){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		SharedPreferences.Editor editor = pref.edit();
		editor.putString("id", id);
		editor.putString("pw", pw);
		editor.commit();
	}
	public static String getId(Context context){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		String id = pref.getString("id", "");
		return id;
	}
	public static String getPw(Context context){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		String pw = pref.getString("pw", "");
		return pw;
	}

	// 로그인 데이터
	public static void setLoginStringData(Context context, String loginData){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		SharedPreferences.Editor editor = pref.edit();
		editor.putString("loginData", loginData);
		editor.commit();
	}
	public static String getLoginStringData(Context context){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		String value = pref.getString("loginData", "");
		return value;
	}

	// DataLogin 리턴
	public static DataLogin getDataLogin(Context context){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		String value = pref.getString("loginData", "");
		try {
			return new DataLogin(new JSONObject(value));
		} catch (JSONException e) {
			e.printStackTrace();
			return null;
		}
	}

	// DataUser 리턴
	public static DataUser getDataUser(Context context){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		String value = pref.getString("loginData", "");
		try {
			DataLogin dataLogin = new DataLogin(new JSONObject(value));
			return new DataUser(dataLogin.getUserDataJsonObject());
		} catch (JSONException e) {
			e.printStackTrace();
			return null;
		}
	}



	// Document 데이터
	public static void setDataDocumentString(Context context, String documentData, String type){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		SharedPreferences.Editor editor = pref.edit();
		editor.putString("document"+type, documentData);
		editor.commit();
	}
	public static String getDocumentStringData(Context context, String type){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		String value = pref.getString("document"+type, "");
		return value;
	}

	// DataDocument 리턴
	public static DataDocument getDataDocument(Context context, String type, int documentId){
		ArrayList<DataDocument> dataDocumentList = getDataDocumentList(context, type);
		for(DataDocument curDataDocument : dataDocumentList){
			if(curDataDocument.getDocumentId() == documentId){
				return curDataDocument;
			}
		}
		return null;
	}

	public static ArrayList<DataDocument> getDataDocumentList(Context context, String type){
		ArrayList<DataDocument> dataDocumentList = new ArrayList<DataDocument>();
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		String value = pref.getString("document"+type, "");
		try {
			JSONObject jsonObjectDocumentList = new JSONObject(value);
			JSONArray jsonArrayDocumentList = jsonObjectDocumentList.getJSONArray("documents");
			for(int i=0; i<jsonArrayDocumentList.length(); i++){
				JSONObject curJsonObject = jsonArrayDocumentList.getJSONObject(i);
				dataDocumentList.add(new DataDocument(curJsonObject));
			}
			return dataDocumentList;
		} catch (JSONException e) {
			e.printStackTrace();
			return null;
		}
	}


	// Notice 데이터
	public static void setDataNoticeString(Context context, String noticeData){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		SharedPreferences.Editor editor = pref.edit();
		editor.putString("noticeList", noticeData);
		editor.commit();			
	}
	public static String getNoticeStringData(Context context){
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		String value = pref.getString("noticeList", "");
		return value;
	}

	public static ArrayList<DataNotice> getDataNoticeList(Context context){
		ArrayList<DataNotice> dataNoticeList = new ArrayList<DataNotice>();
		SharedPreferences pref = context.getSharedPreferences("savedValue", Context.MODE_PRIVATE);
		String value = pref.getString("noticeList", "");
		try {
			JSONObject jsonObjectNoticeList = new JSONObject(value);
			JSONArray jsonArrayNoticeList = jsonObjectNoticeList.getJSONArray("notices");
			for(int i=0; i<jsonArrayNoticeList.length(); i++){
				JSONObject curJsonObject = jsonArrayNoticeList.getJSONObject(i);
				dataNoticeList.add(new DataNotice(curJsonObject));
			}
			return dataNoticeList;
		} catch(JSONException e){
			e.printStackTrace();
			return null;
		}
	}
}
