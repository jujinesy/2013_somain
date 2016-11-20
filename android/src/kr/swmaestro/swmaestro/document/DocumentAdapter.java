package kr.swmaestro.swmaestro.document;

import java.util.ArrayList;

import kr.swmaestro.swmaestro.R;
import kr.swmaestro.swmaestro.data.DataDocumentExtend;
import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

public class DocumentAdapter extends ArrayAdapter<DataDocumentExtend>{
	private String TAG = this.getClass().getSimpleName();
	private Context mContext;
	private ArrayList<DataDocumentExtend> mDocumentExtendList;

	public DocumentAdapter(Context context, int resource, ArrayList<DataDocumentExtend> documentExtendList) {
		super(context, resource, documentExtendList);
		mContext = context;
		mDocumentExtendList = documentExtendList;
//		Log.d(TAG, "DocumentAdapter, list size:" + mDocumentExtendList.size());
	}

	@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		View curView = convertView;
		if(curView == null){
			LayoutInflater inflater = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
			curView = inflater.inflate(R.layout.document_listitem, null);
		}
		TextView tvKey = (TextView) curView.findViewById(R.id.tvDocumentListItemKey);
		TextView tvValue = (TextView) curView.findViewById(R.id.tvDocumentListItemValue);

		DataDocumentExtend curDocumentExtend = mDocumentExtendList.get(position);
		tvKey.setText(curDocumentExtend.getKey());
		tvValue.setText(curDocumentExtend.getValue());
//		Log.d(TAG, "getView : " + curDocumentExtend.getKey() + curDocumentExtend.getValue());

		return curView;
	}
}