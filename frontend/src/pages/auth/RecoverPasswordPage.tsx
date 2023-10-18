import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import './Auth.css';
import { InputTypes } from 'src/types/Input.types';
import Button from 'src/components/Button/Button';
import Input from 'src/components/Input/Input';
import { recoverPassword } from 'src/services/redux/slices/user/user';
import { useAppDispatch } from 'src/services/typeHooks';
import { FieldValues, SubmitHandler, useForm } from 'react-hook-form';
import { EMAIL_VALIDATION_CONFIG } from 'src/utils/constants';

const RecoverPasswordPage = () => {
	const navigate = useNavigate();
	const dispatch = useAppDispatch();

	const [step, setStep] = useState(1);

	const {
		register,
		handleSubmit,
		reset,
		formState: { errors, isDirty, isValid },
		getValues,
	} = useForm({ mode: 'onChange' });

	const onSubmit: SubmitHandler<FieldValues> = () => {
		const userEmail = getValues('email');

		dispatch(recoverPassword(userEmail))
			.unwrap()
			.then((res) => {
				console.log('dispatch recoverPassword success', res);

				setStep(step + 1);
			})
			.catch((err) => {
				console.log('dispatch recoverPassword err:', err);
			});
	};

	return (
		<main className="auth" id="recover-password-page">
			<div className="auth__container">
				<h1 className="auth__title">Восстановить пароль</h1>
				{step === 1 ? (
					<>
						<p className="auth__hint">Введите электронную почту</p>
						<form className="auth__form" onSubmit={handleSubmit(onSubmit)}>
							<Input
								inputType={InputTypes.email}
								labelText="Электронная почта"
								validation={{
									...register('email', EMAIL_VALIDATION_CONFIG),
								}}
								error={errors?.email?.message?.toString()}
							/>
							<Button
								buttonText={'Восстановить'}
								type="submit"
								disabled={!isDirty || !isValid}
							/>
						</form>
					</>
				) : step === 2 ? (
					<>
						<p className="auth__hint">
							Ссылка для восстановления пароля отправлена на указанную почту
						</p>
						<p className="auth__email">{getValues('email')}</p>
						<Button
							buttonText={'Перейти на Главную'}
							handleButtonClick={() => {
								reset();
								navigate('/');
							}}
							type="button"
						/>
					</>
				) : null}
			</div>
		</main>
	);
};

export default RecoverPasswordPage;
