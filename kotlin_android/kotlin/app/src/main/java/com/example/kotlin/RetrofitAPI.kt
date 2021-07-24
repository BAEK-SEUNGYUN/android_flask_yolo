import com.google.gson.JsonObject
import retrofit2.Call
import retrofit2.http.GET

interface RetrofitAPI {
    @GET("/todos")//서버에 GET요청을 할 주소를 입력
    fun getTodoList() : Call<JsonObject> //MainActivity에서 사용할 json파일 가져오는 메서드
}