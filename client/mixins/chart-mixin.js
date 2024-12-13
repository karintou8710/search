import axios from 'axios';

const protocol = process.env.PROTOCOL;
const origin = process.env.ORIGIN;
const bookmarkURL = `${protocol}://${origin}/api/bookmark/`;

const HTTP_201_CREATED = 201;
const HTTP_204_NO_CONTENT = 204;

export default {
    data () {
        return {
            // MainCard
            items: [],
            bookMarkIDs: [],
            isVisible: false,

            chartGridCol: 12,
            query: {
                search: '',
                ordering: '',
                page: 1
            },
            sortItems: [
                { text: '新着順', value: '' },
                { text: 'GPA (降順)', value: '-gpa' },
                { text: 'GPA (昇順)', value: 'gpa' },
                { text: '単位取得者数', value: 'failure' },
                { text: '落単者数', value: '-failure' },
                { text: 'A帯 (降順)', value: '-a_band' },
                { text: 'A帯 (昇順)', value: 'a_band' },
                { text: 'F (降順)', value: '-f' }
            ],
            gridItems: [
                { text: '１列', value: 12 },
                { text: '２列', value: 6 }
            ]
        };
    },
    methods: {
        sort () {
            this.query.page = 1;

            const fullURL = this.joinQuery(this.$route.path);
            this.$router.push(fullURL);
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
        joinQuery (url) {
            let queryURL = '';
            Object.keys(this.query).forEach(
                key => (queryURL += '&' + key + '=' + encodeURIComponent(this.query[key]))
            );
            if (!url.includes('?')) {
                queryURL = queryURL.replace('&', '?'); // 先頭の&を?に置換
            }
            return url + queryURL;
        }
    }
};
