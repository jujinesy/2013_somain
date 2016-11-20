package kr.swmaestro.swmaestro.document;

import kr.swmaestro.swmaestro.other.Pref;

import org.json.JSONException;
import org.json.JSONObject;

import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

public class DocumentListTask extends DocumentListBaseTask{

	public DocumentListTask(Context context, String title, String type) {
		super(context, title, type);
	}

	@Override
	protected void onPostExecute(Integer result) {
		super.onPostExecute(result);
		try {
			JSONObject jsonObjectResult = new JSONObject(resultString);
			
			// Test
			jsonObjectResult.getJSONArray("documents");
			
			Pref.setDataDocumentString(mContext, resultString, type);
			Intent intent = new Intent(mActivity, DocumentListActivity.class);
			intent.putExtra("type", type);
			mActivity.startActivity(intent);
		} catch (JSONException e) {
			e.printStackTrace();
			Toast.makeText(mContext, "서류목록 로딩에 실패하였습니다", Toast.LENGTH_SHORT).show();
		}
	}

}
