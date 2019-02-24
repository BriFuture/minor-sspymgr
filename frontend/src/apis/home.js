import {fetchPost} from './apibase.js'

export const userSignin = function(params) {
    return fetchPost( '/api/home/signin', params);
}

export const sendCheckCode = function(params) {
    return fetchPost( '/api/home/checkcode', params);
}

export const userSignup = function(params) {
    return fetchPost( '/api/home/signup', params);
}

export const isUserSignin = function() {
    return fetchPost( '/api/home/isSignedIn' );
}

export const requestReset = function(params) {
    return fetchPost('/api/home/requestReset', params);
}

export const resetPassword = function(params) {
    return fetchPost('/api/home/resetPassword', params);
}
