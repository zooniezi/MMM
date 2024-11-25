export const piniaResetPlugin = () => {
  return (context) => {
    const initialState = { ...context.options.state() }; // 초기 상태 저장

    context.store.$reset = () => {
      Object.assign(context.store.$state, initialState); // 상태를 초기값으로 리셋
    };
  };
};
