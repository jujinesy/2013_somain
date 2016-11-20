package kr.swmaestro.swmaestro.document;

import java.util.ArrayList;

import kr.swmaestro.swmaestro.R;
import kr.swmaestro.swmaestro.data.DataDocument;
import kr.swmaestro.swmaestro.other.CommonFunction;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

public class DocumentListAdapter extends ArrayAdapter<DataDocument>{
	private String TAG = this.getClass().getSimpleName();
	private Context mContext;
	private ArrayList<DataDocument> mDataDocumentList;
	private int res;
	
	public DocumentListAdapter(Context context, int resource, ArrayList<DataDocument> dataDocumentList) {
		super(context, resource, dataDocumentList);
		mContext = context;
		mDataDocumentList = dataDocumentList;
		res = resource;
	}

	@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		View curView = convertView;
		if(curView == null){
			LayoutInflater inflater = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
			curView = inflater.inflate(res, null);
		}
		TextView tvType = (TextView) curView.findViewById(R.id.tvDocumentListItemType);
		TextView tvDeadline = (TextView) curView.findViewById(R.id.tvDocumentListItemDeadline);
		TextView tvUserList = (TextView) curView.findViewById(R.id.tvDocumentListItemSignUserList);
		TextView tvSignedUserList = (TextView) curView.findViewById(R.id.tvDocumentListItemSignedUserList);
		ImageView ivDone = (ImageView) curView.findViewById(R.id.ivDocumentListItemDone);
		
		DataDocument curDataDocument = mDataDocumentList.get(position);
		
		tvType.setText(curDataDocument.getDocumentType());
		tvDeadline.setText(curDataDocument.getDeadLine());
		tvUserList.setText(CommonFunction.getUserListString(curDataDocument.getSignUserList()));
		tvSignedUserList.setText(CommonFunction.getUserListString(curDataDocument.getSignedUserList()));
		if(! curDataDocument.isSubmitted()){
			ivDone.setVisibility(View.GONE);
		}
		
		return curView;
	}
}