<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">회원정보 수정</h1>

    <!-- 프로필 수정 폼 -->
    <div class="card shadow p-4">
      <h3 class="mb-3">프로필 수정</h3>
      <form @submit.prevent="updateProfile" @keyup.enter="updateProfile">
        <div class="mb-3">
          <label for="profile" class="form-label">프로필 소개</label>
          <textarea
            id="profile"
            class="form-control"
            rows="5"
            v-model="userProfile"
            placeholder="자신을 소개해주세요"
          ></textarea>
        </div>
        <button type="submit" class="btn btn-primary w-100">저장</button>
      </form>
    </div>

    <!-- 회원 탈퇴 -->
    <div class="text-center mt-4">
      <button class="btn btn-danger w-100" @click="deleteUser">회원 탈퇴</button>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useMovieStore } from "@/stores/movie";
import { useRouter } from "vue-router";

const store = useMovieStore();
const router = useRouter();
const SERVER_API_URL = store.SERVER_API_URL;

// 상태 변수
const userId = ref(null);
const userProfile = ref("");

// 사용자 ID 및 프로필 불러오기
const getUserId = async function () {
  try {
    const res = await axios({
      method: "get",
      url: `${SERVER_API_URL}/accounts/userinfo/${store.userName}/`,
      headers: {
        Authorization: `Token ${store.serverToken}`,
      },
    });
    userId.value = res.data.id;
    userProfile.value = res.data.profile; // 프로필 데이터 저장
  } catch (err) {
    console.error("사용자 정보를 불러오는 중 문제가 발생했습니다.", err);
  }
};

// 프로필 업데이트
const updateProfile = async function () {
  try {
    await axios({
      method: "put",
      url: `${SERVER_API_URL}/accounts/profile/update/`, // API 엔드포인트
      headers: {
        Authorization: `Token ${store.serverToken}`,
      },
      data: {
        profile: userProfile.value, // 수정된 프로필 데이터 전송
      },
    });
    alert("프로필이 성공적으로 수정되었습니다.");
    router.push({ name: 'myPage' })
  } catch (err) {
    console.error("프로필 수정 중 문제가 발생했습니다.", err);
    alert("프로필 수정에 실패했습니다.");
  }
};

// 회원 탈퇴
const deleteUser = async function () {
  if (confirm("정말로 회원 탈퇴를 진행하시겠습니까?")) {
    try {
      await axios({
        method: "delete",
        url: `${SERVER_API_URL}/accounts/delete/`,
        headers: {
          Authorization: `Token ${store.serverToken}`,
        },
      });
      alert("회원 탈퇴가 완료되었습니다.");
      store.serverToken = null; // 토큰 제거
      router.push({ name: "logIn" }); // 로그인 페이지로 이동
    } catch (err) {
      console.error("회원 탈퇴 중 문제가 발생했습니다.", err);
      alert("회원 탈퇴에 실패했습니다.");
    }
  }
};

// 컴포넌트 로드 시 사용자 정보 불러오기
onMounted(() => {
  getUserId();
});
</script>

<style scoped>
/* 부트스트랩 스타일을 활용하여 추가적인 커스터마이징 */
.card {
  max-width: 600px;
  margin: 0 auto;
}
textarea {
  resize: none; /* 텍스트 박스 크기 조정 방지 */
}
</style>
