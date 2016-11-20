package kr.swmaestro.swmaestro.notice;

import java.util.ArrayList;

import kr.swmaestro.swmaestro.R;
import kr.swmaestro.swmaestro.data.DataNotice;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

public class NoticeListAdapter extends ArrayAdapter<DataNotice>{
	private Context mContext;
	private int resource;
	private ArrayList<DataNotice> mDataNoticeList;

	public NoticeListAdapter(Context context, int resource, ArrayList<DataNotice> dataNoticeList) {
		super(context, resource, dataNoticeList);
		mContext = context;
		this.resource = resource;
		mDataNoticeList = dataNoticeList;
	}

	@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		View curView = convertView;
		if(curView == null){
			LayoutInflater inflater = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
			curView = inflater.inflate(resource, null);
		}
		
		TextView tvCategory = (TextView) curView.findViewById(R.id.tvNoticeListListItemCategory);
		TextView tvDate = (TextView) curView.findViewById(R.id.tvNoticeListListItemDate);
		TextView tvTitle = (TextView) curView.findViewById(R.id.tvNoticeListListItemTitle);
		
		DataNotice curDataNotice = mDataNoticeList.get(position);
		tvCategory.setText(curDataNotice.getCategory());
		tvDate.setText(curDataNotice.getCreatedDate());
		tvTitle.setText(curDataNotice.getTitle());
		
		return curView;
	}
}
