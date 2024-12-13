<template>
    <v-container>
        <!-- pagination -->
        <v-row>
            <v-col>
                <Pagination
                    :size="size"
                    :total-visible="totalVisible"
                    :current-page="currentPage"
                    :count="count"
                    @updatePage="setPageAndGetData"
                    @input="(page) => (currentPage = page)"
                />
            </v-col>
        </v-row>

        <client-only>
            <!-- 表示・検索機能 PC -->
            <v-row class="d-none d-sm-flex">
                <v-col cols="5">
                    <v-text-field
                        v-model="search"
                        clearable
                        outlined
                        label="講義を検索する"
                        prepend-inner-icon="mdi-magnify"
                        clear-icon="mdi-close-circle"
                        hint="講義名・教員名・年度・学部・クラスなどで検索ができます。"
                        autocomplete="off"
                        @keydown.enter="filterSearch"
                    />
                </v-col>

                <v-spacer />

                <v-col cols="2">
                    <v-select
                        v-model="chartGridCol"
                        prepend-icon="mdi-grid-large"
                        :items="gridItems"
                        label="grid"
                    />
                </v-col>

                <v-col cols="2">
                    <v-select
                        v-model="query.ordering"
                        prepend-icon="mdi-sort-descending"
                        :items="sortItems"
                        label="Sort"
                        @change="sort"
                    />
                </v-col>
            </v-row>

            <!-- 表示・検索機能 スマホ -->
            <v-row class="d-sm-none">
                <v-col cols="12">
                    <v-text-field
                        v-model="search"
                        class="mx-5"
                        label="講義を検索する"
                        clearable
                        outlined
                        prepend-inner-icon="mdi-magnify"
                        clear-icon="mdi-close-circle"
                        hint="講義名・教員名・年度・学部・クラスなどで検索ができます。"
                        @keydown.enter="filterSearch"
                    />
                </v-col>
            </v-row>

            <v-row class="d-sm-none">
                <v-spacer />

                <v-col
                    cols="6"
                    class="mx-5"
                >
                    <v-select
                        v-model="query.ordering"
                        prepend-icon="mdi-sort-descending"
                        label="Sort"
                        :items="sortItems"
                        @change="sort"
                    />
                </v-col>
            </v-row>

            <v-row class="d-sm-none">
                <v-spacer />
            </v-row>
        </client-only>

        <!-- Alert-->
        <v-row>
            <v-col>
                <v-alert
                    v-if="searchResultText"
                    type="success"
                >
                    検索結果：{{ searchResultText }}
                </v-alert>
            </v-col>
        </v-row>

        <!-- main cards -->
        <v-row>
            <template v-if="!isVisible">
                <v-col
                    v-for="i in 10"
                    :key="i"
                    :cols="chartGridCol"
                >
                    <SkeletonCard />
                </v-col>
            </template>
            <template v-else>
                <v-col
                    v-for="(item, index) in items"
                    :key="item.id"
                    :cols="chartGridCol"
                >
                    <Card
                        :item="item"
                        :index="index"
                        @starClick="postBookMark(index)"
                    />
                </v-col>
            </template>
        </v-row>

        <!-- pagination -->
        <v-row>
            <v-col>
                <Pagination
                    :size="size"
                    :total-visible="totalVisible"
                    :current-page="currentPage"
                    :count="count"
                    @updatePage="setPageAndGetData"
                    @input="(page) => (currentPage = page)"
                />
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';
import MobileDetect from 'mobile-detect';
import chartMixin from '@/mixins/chart-mixin';

const protocol = process.env.PROTOCOL;
const origin = process.env.ORIGIN;
const gradeURL = `${protocol}://${origin}/api/gradeinfo/`;
const bookmarkURL = `${protocol}://${origin}/api/bookmark/`;

export default {
    mixins: [chartMixin],
    beforeRouteUpdate (to, from, next) {
    // クエリなしに対応
        this.query.page = to.query.page || 1;
        this.query.ordering = to.query.ordering || '';
        this.query.search = to.query.search || '';
        window.scrollTo(0, 0);
        this.fetchGradeAPIData();
        next();
    },
    data () {
        return {
            // Pagination
            currentPage: 1,
            totalVisible: 0,
            size: 0,
            count: null,

            search: '',
            searchResultText: null
        };
    },
    async fetch () {
        if (this.$route.fullpath !== '/service') {
            this.query.page = this.$route.query.page || 1;
            this.query.ordering = this.$route.query.ordering || '';
            this.query.search = this.$route.query.search || '';
            this.search = this.$route.query.search || '';
        }

        await this.fetchGradeAPIData();

        if (process.server) {
            const headers = this.$nuxt.context.req.headers;
            await this.fetchBookmarkAPIData(headers);
            const md = new MobileDetect(headers['user-agent']);
            this.chartGridCol = md.mobile() ? 12 : 6;
            this.totalVisible = md.mobile() ? 5 : 10;
        } else {
            await this.fetchBookmarkAPIData();
        }
    },
    head () {
        return {
            title: `${this.query.search ? this.query.search + ' - ' : ''}成績検索`
        };
    },
    mounted () {
        // 画面サイズがxsなら表示個数を減らす
        this.totalVisible = window.innerWidth <= 600 ? 5 : 10;
        this.chartGridCol = window.innerWidth <= 600 ? 12 : 6;
    },
    methods: {
        filterSearch () {
            // vuetifyのclearはnullが挿入される
            this.query.search = this.search || '';
            this.query.page = 1;

            const fullURL = this.joinQuery(this.$route.path);
            this.$router.push(fullURL);
        },

        setPageAndGetData (page) {
            if (page <= 0 || page > this.size) { return; }
            if (page === this.query.page) { return; }
            this.query.page = page;
            window.scrollTo(0, 0);

            const fullURL = this.joinQuery(this.$route.path);
            if (this.$route.path !== fullURL) {
                this.$router.push(fullURL);
            }
        },

        async fetchGradeAPIData () {
            this.isVisible = false;

            let res;
            try {
                res = await axios.get(this.joinQuery(gradeURL), {
                    withCredentials: true
                });
            } catch (error) {
                if (error.response) {
                    this.$nuxt.error({
                        status: error.response.status,
                        message: 'サーバーでエラーが発生しました'
                    });
                } else if (error.request) {
                    this.$nuxt.error({
                        message: 'サーバーからレスポンスがありません'
                    });
                } else {
                    this.$nuxt.error({
                        message: error.message
                    });
                }
                return;
            }

            // 取得したデータがブックマークされているか確認
            res.data.results.forEach((item) => {
                item.isBookMark = this.bookMarkIDs.includes(item.id);
            });
            // chartを更新
            this.items.splice(0, this.items.length);
            this.items.push(...res.data.results);
            this.size = res.data.size;
            this.count = res.data.count;
            this.currentPage = Number(this.query.page);
            this.searchResultText = this.query.search;

            // 取得したデータがブックマークされているか確認

            this.isVisible = true;
        },

        // ページに訪れた時のみに使用
        async fetchBookmarkAPIData (headers) {
            const options = {
                withCredentials: true
            };
            if (headers) { options.headers = { cookie: headers.cookie }; }
            let res;
            try {
                res = await axios.get(bookmarkURL, options);
            } catch (error) {
                if (error.response) {
                    this.$nuxt.error({
                        status: error.response.status,
                        message: 'サーバーでエラーが発生しました'
                    });
                } else if (error.request) {
                    this.$nuxt.error({
                        message: 'サーバーからレスポンスがありません'
                    });
                } else {
                    this.$nuxt.error({
                        message: error.message
                    });
                }
                return;
            }
            this.bookMarkIDs = res.data.map(item => item.id);
            this.items.forEach((item) => {
                this.$set(item, 'isBookMark', this.bookMarkIDs.includes(item.id));
            });
        }
    }
};
</script>
