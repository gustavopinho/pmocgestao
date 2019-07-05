var gulp = require('gulp');
var sass = require('gulp-sass');
var minifyCss = require('gulp-csso')
/*var minifyJs = require('gulp-uglify')*/
var minifyJs = require('gulp-uglify-es').default
var cleanCSS = require('gulp-clean-css');
var jshint = require('gulp-jshint');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var browserSync = require('browser-sync').create();

var paths_copy_js = [
    'node_modules/admin-lte/plugins/jQuery/jquery-2.2.3.min.js',
    'node_modules/admin-lte/plugins/jQueryUI/jquery-ui.min.js',
    'node_modules/admin-lte/plugins/input-mask/jquery.inputmask.js',
    'node_modules/admin-lte/bootstrap/js/bootstrap.min.js',
    'node_modules/admin-lte/plugins/fastclick/fastclick.min.js',
    'node_modules/admin-lte/plugins/select2/select2.full.min.js',
    'node_modules/admin-lte/plugins/datepicker/bootstrap-datepicker.js',
    'node_modules/admin-lte/plugins/datepicker/locales/bootstrap-datepicker.pt-BR.js',
    'node_modules/moment/min/moment.min.js',
    'node_modules/chart.js/dist/chart.min.js',
    'node_modules/chart.js/dist/Chart.bundle.min.js',
    'node_modules/admin-lte/plugins/fullcalendar/fullcalendar.min.js',
    'node_modules/bootbox/bootbox.min.js',
    'node_modules/admin-lte/dist/js/app.min.js',
];

var paths_copy_css = [
    'node_modules/admin-lte/bootstrap/css/bootstrap.min.css',
    'node_modules/admin-lte/plugins/select2/select2.min.css',
    'node_modules/admin-lte/plugins/datepicker/datepicker3.css',
    'node_modules/font-awesome/css/font-awesome.min.css',
    'node_modules/ionicons/dist/css/ionicons.min.css',
    'node_modules/admin-lte/plugins/fullcalendar/fullcalendar.min.css',
    'node_modules/admin-lte/dist/css/AdminLTE.min.css',
    'node_modules/admin-lte/dist/css/skins/skin-black-light.min.css',


];

var paths_copy_fonts = [
    'node_modules/admin-lte/bootstrap/fonts/*',
    'node_modules/font-awesome/fonts/*',
    'node_modules/ionicons/dist/fonts/*',
];


var paths_vue = [
    'node_modules/vue/dist/vue.min.js',
    'node_modules/vue-chartjs/dist/vue-chartjs.js',
    'node_modules/vue-resource/dist/vue-resource.min.js',
]

// Paths
var paths_html_py = [
  "./{core,empresa,cliente}/**/*.{html,py}",
  "./{core,empresa,cliente}/**/**/*.{html,py}",
  "./{core,empresa,cliente}/**/**/**/*.{html,py}",
];

var paths_scss = [
  './assets/sass/*.scss',
];

var paths_js = [
  './assets/js/*.js'
];

var paths_img = [
  './assets/img/**'
];

// Copy Js
gulp.task('copy_js', function() {
  return gulp.src(paths_copy_js)
    .pipe(concat('vendor.js'))
    .pipe(minifyJs())
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest('core/static/js'));
});

// Copy Css
gulp.task('copy_css', function() {
  return gulp.src(paths_copy_css)
    .pipe(concat('vendor.css'))
    .pipe(minifyCss())
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest('core/static/css'));
});

// Ckeditor
gulp.task('copy_img', function() {
  return gulp.src(paths_img)
    .pipe(gulp.dest('core/static/img'));
});

// Vue
gulp.task('copy_vue', function() {
  return gulp.src(paths_vue)
    .pipe(concat('vue.js'))
    .pipe(minifyJs())
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest('core/static/js'));
});

// Copy Fonts
gulp.task('copy_fonts', function() {
    return gulp.src(paths_copy_fonts)
            .pipe(gulp.dest('core/static/fonts/'));
});

// Compile Our Sass
gulp.task('sass', function() {
    return gulp.src(paths_scss)
        .pipe(sass())
        .pipe(cleanCSS({ compatibility: 'ie8' }))
        .pipe(gulp.dest('./core/static/css/'))
        .pipe(rename({ suffix: '.min' }))
        .pipe(minifyCss())
        .pipe(gulp.dest('./core/static/css'))
        .pipe(browserSync.reload({stream: true}));
});

// Concatenate & Minify JS
gulp.task('js', function() {
    return gulp.src(paths_js)
        .pipe(jshint())
        .pipe(jshint.reporter('default'))
        .pipe(gulp.dest('./core/static/js'))
        .pipe(rename({ suffix: '.min' }))
        .pipe(minifyJs())
        .pipe(gulp.dest('./core/static/js'))
        .pipe(browserSync.reload({stream: true}));
});

// Watch Files For Changes
gulp.task('watch', function() {

    browserSync.init({
        notify: false,
        proxy: "[::]:8000"
    });

    gulp.watch(paths_js, ['js']);
    gulp.watch('assets/img/**', ['copy_img']);
    gulp.watch('assets/sass/*.scss', ['sass']);    

    gulp.watch(paths_html_py).on('change', browserSync.reload);
});

// Production Tasks
gulp.task('production', ['copy_js', 'copy_css', 'copy_img', 'copy_vue','copy_fonts','sass', 'js'])

// Default Tasks
gulp.task('default', ['copy_js', 'copy_css', 'copy_img', 'copy_vue', 'copy_fonts', 'sass', 'js', 'watch']);
