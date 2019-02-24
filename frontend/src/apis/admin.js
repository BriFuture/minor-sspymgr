import {fetchPost} from './apibase.js'

export const getAllProducts = function(params) {
    return fetchPost('/api/admin/product/getAll', params);
}

export const getProduct = function(params) {
    return fetchPost('/api/admin/product/get', params);
}

export const updateProduct = function(params) {
    return fetchPost('/api/admin/product/update', params);
}


export const updateProductQrcode = function(params) {
    return fetchPost('/api/admin/productQrcode/update', params);
}

export const deleteProductQrcode = function(params) {
    return fetchPost('/api/admin/productQrcode/delete', params);
}

export const getAllUser = function(params) {
    return fetchPost('/api/admin/user/getAll', params);
}

export const getUserDetail = function(params) {
    return fetchPost('/api/admin/user/getDetail', params);
}

export const getAllAccount = function(params) {
    return fetchPost('/api/admin/account/get', params);
}

export const getAccountDetail = function(params) {
    return fetchPost('/api/admin/account/getDetail', params)
}

export const getOrderHistory = function(params) {
    return fetchPost('/api/admin/orderHistory/get', params)
}

export const getAllSettings = function(params) {
    return fetchPost('/api/admin/setting/getAll', params)
}

export const getAllEmails = function(params) {
    return fetchPost('/api/admin/email/getAll', params);
}

export const getEmailHistory = function(params) {
    return fetchPost('/api/admin/email/getPage', params);
}


export const getDayFlowUsage = function(params) {
    return fetchPost('/api/admin/flowUsage/getInDay', params)
}

export const getMonFlowUsage = function(params) {
    return fetchPost('/api/admin/flowUsage/getInMon', params)
}

// ==================

export const randomAccountPassword = function(params) {
    return fetchPost('/api/admin/account/randomPassword', params)
}

export const updateAccountPassword = function(params) {
    return fetchPost('/api/admin/account/updatePassword', params)
}

export const updateAccountFlow = function(params) {
    return fetchPost('/api/admin/account/updateTotalFlow', params)
}

export const updateAccountExpiration = function(params) {
    return fetchPost('/api/admin/account/updateExpiration', params)
}

export const updateUserBasicInfo = function(params) {
    return fetchPost('/api/admin/user/updateInfo', params);
}

export const createAnnouncement = function(params) {
    return fetchPost('/api/admin/announcement/create', params);
}

export const getAnnouncements = function(params) {
    return fetchPost('/api/admin/announcement/getAll', params);
}

export const delAnnouncement = function(params) {
    return fetchPost('/api/admin/announcement/delete', params);
}