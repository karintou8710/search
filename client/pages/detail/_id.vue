<template>
    <v-container>
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
        </client-only>

        <!-- Alert-->
        <v-row>
            <v-col>
                <v-alert
                    type="info"
                >
                    詳細ページ
                </v-alert>
            </v-col>
        </v-row>

        <!-- main cards -->
        <v-row>
            <template v-if="!isVisible">
                <v-col>
                    <SkeletonCard />
                </v-col>
            </template>
            <template v-else>
                <v-col
                    v-for="(item, index) in items"
                    :key="item.id"
                >
                    <Card
                        :item="item"
                        :index="index"
                        @starClick="postBookMark(index)"
                    />
                </v-col>
            </template>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';

const protocol = process.env.PROTOCOL;
const origin = process.env.ORIGIN;
const ogpDomain = 'inazo-ogp-image.vercel.app';
const gradeURL = `${protocol}://${origin}/api/gradeinfo/`;
const bookmarkURL = `${protocol}://${origin}/api/bookmark/`;

const HTTP_201_CREATED = 201;
const HTTP_204_NO_CONTENT = 204;

const E = (component) => {
    return encodeURIComponent(component);
};

export default {
    data () {
        return {
            // MainCard
            // itemsは1個まで
            items: [],
            bookMarkIDs: [],
            isVisible: false,

            search: '',

            query: {
                search: '',
                ordering: '',
                page: 1
            },

            ogpInfo: {
                title: '',
                subtitle: '',
                data: []
            }
        };
    },
    async fetch () {
        await this.fetchGradeAPIData();

        if (process.server) {
            const headers = this.$nuxt.context.req.headers;
            await this.fetchBookmarkAPIData(headers);
        } else {
            await this.fetchBookmarkAPIData();
        }
    },
    head () {
        return {
            title: this.items[0]?.subject || '',
            meta: [
                {
                    hid: 'og:description',
                    name: 'og:description',
                    content: `${this.ogpInfo.title} / ${this.ogpInfo.subtitle}`
                },
                {
                    hid: 'twitter:image',
                    name: 'twitter:image',
                    content: this.ogpImageURL
                },
                {
                    hid: 'twitter:card',
                    name: 'twitter:card',
                    content: 'summary_large_image'
                },
                {
                    hid: 'og:image',
                    name: 'og:image',
                    content: this.ogpImageURL
                }
            ]
        };
    },
    computed: {
        ogpImageURL () {
            const url = `https://${ogpDomain}/inazo-ogp-image.vercel.app/?data=${E(this.ogpInfo.data.join(','))}&title=${E(this.ogpInfo.title)}&subtitle=${E(this.ogpInfo.subtitle)}`;
            return url;
        }
    },
    methods: {
        filterSearch () {
            this.$router.push({ path: `/search/?search=${this.search}` });
        },

        async fetchGradeAPIData () {
            this.isVisible = false;

            let res;
            try {
                res = await axios.get(gradeURL + this.$route.params.id, {
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

            // chartを更新
            this.items.push(res.data);

            // 取得したデータがブックマークされているか確認
            this.items.forEach((item) => {
                item.isBookMark = this.bookMarkIDs.includes(item.id);
            });

            // ogp情報の設定
            if (res.data.subject === ' ') {
                this.ogpInfo.title = res.data.lecture;
            } else {
                this.ogpInfo.title = `${res.data.subject} ${res.data.lecture !== ' ' ? res.data.lecture : ''}`;
            }

            this.ogpInfo.subtitle = `${res.data.year}年度${res.data.semester}`;
            this.ogpInfo.subtitle += (res.data.group !== ' ') ? ` / ${res.data.group} ` : '';
            this.ogpInfo.subtitle += (res.data.teacher !== ' ') ? ` / ${res.data.teacher}` : '';
            this.ogpInfo.subtitle += ` / ${res.data.numOfStudents}人`;
            this.ogpInfo.subtitle += ` / GPA:${res.data.gpa}`;

            this.ogpInfo.data = [
                res.data.ap, res.data.a, res.data.am,
                res.data.bp, res.data.b, res.data.bm,
                res.data.cp, res.data.c, res.data.d,
                res.data.dm, res.data.f
            ];

            this.isVisible = true;
        },

        async postBookMark (index) {
            // Objectをコピーする必要がある。
            const item = Object.assign({}, this.items[index]);
            const bookMarkID = item.id;

            if (item.isBookMark) {
                // ブックマーク解除
                let res;
                try {
                    res = await axios.delete(`${bookmarkURL}${bookMarkID}/`, {
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

                if (res.status === HTTP_204_NO_CONTENT) {
                    this.bookMarkIDs = this.bookMarkIDs.filter(id => id !== bookMarkID);
                    item.isBookMark = !item.isBookMark;
                    this.$set(this.items, index, item);
                } else {
                    this.$nuxt.error({
                        status: res.status,
                        message: '予期しないステータスコードです'
                    });
                }
            } else {
                // 登録
                let res;
                try {
                    res = await axios.post(
                        bookmarkURL,
                        { bookMarkID },
                        {
                            withCredentials: true
                        }
                    );
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

                if (res.status === HTTP_201_CREATED) {
                    this.bookMarkIDs = res.data.bookMarkIDs;
                    item.isBookMark = !item.isBookMark;
                    this.$set(this.items, index, item);
                } else {
                    this.$nuxt.error({
                        status: res.status,
                        message: '予期しないステータスコードです'
                    });
                }
            }
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
