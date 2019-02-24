import {fetchPost} from './apibase.js'

export const getUserAccount = function(params) {
    return fetchPost('/api/user/accountDetail', params);
}

export const updateUserPassword = function(params) {
    return fetchPost('/api/user/updatePassword', params);
}

export const updateAccountPassword = function(params) {
    return fetchPost('/api/user/account/updatePassword', params);
}

export const getAvailableProducts = function(params) {
    return fetchPost('/api/user/product/getAll', params);
}

export const canPlaceOrder = function(params) {
    return fetchPost('/api/user/product/canPlace', params);
}

export const getProductDetail = function(params) {
    return fetchPost('/api/user/product/getDetail', params);
}

export const getDayFlowUsage = function(params) {
    return fetchPost('/api/user/flowUsage/getInDay', params)
}

export const getMonFlowUsage = function(params) {
    return fetchPost('/api/user/flowUsage/getInMon', params)
}

export const getAnnouncements = function(params) {
    return fetchPost('/api/user/announcement/getAll', params)
}
// ====================

export const confirmOrder = function(params) {
    return fetchPost('/api/user/product/confirm', params);
}

export const getOrderHistory = function(params) {
    return fetchPost('/api/user/orderHistory/get', params);
}