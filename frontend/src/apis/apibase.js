import $ from 'jquery'

export function fetchGet(url, params = {}) {
    return new Promise((resolve, reject) => {
        $.get(url, params).then( resp => {
            resolve( resp );
        }).catch( error => {
            reject( error );
        });
    });
}

export function fetchPost(url, params = {}) {
    return new Promise((resolve, reject) => {
        $.post(url, params).then( resp => {
            resolve( resp );
        }).catch( error => {
            reject( error );
        });
    });
}

export const toSignout = function(params) {
    return fetchPost('/api/user/signout', params);
}
