const jwt = require('jsonwebtoken');

module.exports = auth;

function auth(roles = []) {
    
    if (typeof roles === 'string') {
        roles = [roles];
    }

    return function(req, res, next) {
        // Get the token from the header
        const token = req.header('x-auth-token');

        // Check if no token
        if (!token){
            return res.status(401).json({
                message: 'No token, authorization denied'
            });
        }

        // Verify token
        try{
            const decoded = jwt.verify(token, process.env.JWT_TOKEN);
            req.user = decoded.user;
            if (roles.length && !roles.includes(req.user.role)) {
                // user's role is not authorized
                return res.status(401).json({ message: 'Restricted Access' });
            }
            next();
        } catch(err){
            console.log(err);
            res.status(401).json({
                message: 'Token is not valid'
            });
        }
    }
}
