package kr.swmaestro.swmaestro.notice;

import java.util.HashMap;

import kr.swmaestro.swmaestro.other.BaseAsyncTask;
import kr.swmaestro.swmaestro.other.C;
import kr.swmaestro.swmaestro.other.Pref;

import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

public class NoticeTask extends BaseAsyncTask {
	private Context mContext;
	private Activity mActivity;
	private String resultString;

	public NoticeTask(Context context, String title) {
		super(context, title);
		mContext = context;
		mActivity = (Activity) mContext;
	}

	@Override
	protected Integer doInBackground(Void... params) {
		HashMap<String, String> map = new HashMap<String, String>();
		map.put("session_key", Pref.getDataLogin(mContext).getSessionKey());
		map.put("username", Pref.getDataUser(mContext).getUserName());
		
		resultString = postRequest(C.API_NOTICE_LIST, map);
		return super.doInBackground(params);
	}
	
	@Override
	protected void onPostExecute(Integer result) {
		super.onPostExecute(result);
		try{
			JSONObject jsonObjectResult = new JSONObject(resultString);
			
			// Test
			jsonObjectResult.getJSONArray("notices");
			
			Pref.setDataNoticeString(mContext, resultString);
			Intent intent = new Intent(mActivity, NoticeListActivity.class);
			mActivity.startActivity(intent);
		} catch(JSONException e){
			e.printStackTrace();
			Toast.makeText(mContext, "공지사항 목록 로딩에 실패하였습니다", Toast.LENGTH_SHORT).show();
		}
	}
	
}
