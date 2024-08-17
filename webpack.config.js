const path = require('path');

module.exports = {
    entry: './frontend/index.js',  // точка входа для вашего кода
    output: {
        path: path.resolve(__dirname, 'static/frontend'),  // путь вывода для скомпилированных файлов
        filename: 'index.js',  // имя файла вывода
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react']
                    }
                }
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            },
        ],
    },
    resolve: {
        extensions: ['.js', '.jsx']
    },
    mode: 'development'
};
