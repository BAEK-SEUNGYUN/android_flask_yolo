package com.example.kotlin

//import android.support.v7.app.AppCompatActivity

import RetrofitAPI
import android.os.Bundle
import android.util.Log
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import com.google.gson.Gson
import com.google.gson.JsonObject
import kotlinx.android.synthetic.main.activity_main.*
import retrofit2.Call
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class MainActivity : AppCompatActivity() {

    val TAG = "TAG_MainActivity"

    lateinit var mRetrofit :Retrofit
    lateinit var mRetrofitAPI: RetrofitAPI
    lateinit var mCallTodoList : retrofit2.Call<JsonObject>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        setRetrofit()

        //버튼 클릭하면 가져오기
        flask_btn.setOnClickListener {
            flask_btn.visibility = View.INVISIBLE
            proBar.visibility = View.VISIBLE
            callTodoList()
        }
    }


    // 리스트를 불러온다.
    private fun callTodoList() {
        mCallTodoList = mRetrofitAPI.getTodoList()
        mCallTodoList.enqueue(mRetrofitCallback)//응답을 큐 대기열에 넣는다.
    }

    //http요청을 보냈고 이건 응답을 받을 콜벡메서드
    private val mRetrofitCallback  = (object : retrofit2.Callback<JsonObject>{
        override fun onFailure(call: Call<JsonObject>, t: Throwable) {
            t.printStackTrace()
            Log.d(TAG, "에러입니다. => ${t.message.toString()}")
            flask_data.text = "에러\n" + t.message.toString()

            proBar.visibility = View.GONE
            flask_btn.visibility = View.VISIBLE
        }

        override fun onResponse(call: Call<JsonObject>, response: Response<JsonObject>) {
            val result = response.body()
            Log.d(TAG, "결과는 => $result")


            var mGson = Gson()
            val dataParsed1 = mGson.fromJson(result, DataModel.TodoInfo1::class.java)
            val dataParsed2 = mGson.fromJson(result, DataModel.TodoInfo2::class.java)
            val dataParsed3 = mGson.fromJson(result, DataModel.TodoInfo3::class.java)

            flask_data.text = "해야할 일\n" + dataParsed1.todo1.task+"\n"+dataParsed2.todo2.task +"\n"+dataParsed3.todo3.task

            proBar.visibility = View.GONE
            flask_btn.visibility = View.VISIBLE
        }
    })

    private fun setRetrofit(){
        //레트로핏으로 가져올 url설정하고 세팅
        mRetrofit = Retrofit
            .Builder()
            .baseUrl(getString(R.string.baseUrl))
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        //인터페이스로 만든 레트로핏 api요청 받는 것 변수로 등록
        mRetrofitAPI = mRetrofit.create(RetrofitAPI::class.java)
    }

}